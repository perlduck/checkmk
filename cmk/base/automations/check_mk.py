#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import abc
import ast
import functools
import glob
import io
import itertools
import json
import logging
import operator
import os
import shlex
import shutil
import socket
import subprocess
import sys
import time
import uuid
from collections.abc import Callable, Container, Iterable, Iterator, Mapping, Sequence
from contextlib import redirect_stderr, redirect_stdout, suppress
from dataclasses import asdict, dataclass
from itertools import chain, islice
from pathlib import Path
from typing import Any

import livestatus

import cmk.ccc.debug
from cmk.ccc import version
from cmk.ccc.exceptions import MKBailOut, MKGeneralException, MKSNMPError, MKTimeout, OnError
from cmk.ccc.version import edition_supports_nagvis

import cmk.utils.password_store
import cmk.utils.paths
from cmk.utils import config_warnings, ip_lookup, log, man_pages, tty
from cmk.utils.agentdatatype import AgentRawData
from cmk.utils.auto_queue import AutoQueue
from cmk.utils.caching import cache_manager
from cmk.utils.config_path import LATEST_CONFIG
from cmk.utils.diagnostics import deserialize_cl_parameters, DiagnosticsCLParameters
from cmk.utils.encoding import ensure_str_with_fallback
from cmk.utils.everythingtype import EVERYTHING
from cmk.utils.hostaddress import HostAddress, HostName, Hosts
from cmk.utils.labels import DiscoveredHostLabelsStore, HostLabel
from cmk.utils.log import console
from cmk.utils.macros import replace_macros_in_str
from cmk.utils.paths import (
    autochecks_dir,
    autodiscovery_dir,
    base_autochecks_dir,
    base_discovered_host_labels_dir,
    counters_dir,
    data_source_cache_dir,
    discovered_host_labels_dir,
    local_agent_based_plugins_dir,
    local_checks_dir,
    logwatch_dir,
    nagios_startscript,
    omd_root,
    precompiled_hostchecks_dir,
    snmpwalks_dir,
    tcp_cache_dir,
    tmp_dir,
    var_dir,
)
from cmk.utils.rulesets.ruleset_matcher import RulesetMatcher, RuleSpec
from cmk.utils.sectionname import SectionName
from cmk.utils.servicename import Item, ServiceName
from cmk.utils.timeout import Timeout
from cmk.utils.timeperiod import load_timeperiods, timeperiod_active

from cmk.automations.results import (
    ActiveCheckResult,
    AnalyseHostResult,
    AnalyseServiceResult,
    AnalyzeHostRuleMatchesResult,
    AnalyzeServiceRuleMatchesResult,
    AutodiscoveryResult,
    CreateDiagnosticsDumpResult,
    DeleteHostsKnownRemoteResult,
    DeleteHostsResult,
    DiagHostResult,
    DiagSpecialAgentHostConfig,
    DiagSpecialAgentInput,
    DiagSpecialAgentResult,
    DiscoveredHostLabelsDict,
    GetAgentOutputResult,
    GetCheckInformationResult,
    GetConfigurationResult,
    GetSectionInformationResult,
    GetServiceNameResult,
    GetServicesLabelsResult,
    NotificationAnalyseResult,
    NotificationGetBulksResult,
    NotificationReplayResult,
    NotificationTestResult,
    ReloadResult,
    RenameHostsResult,
    RestartResult,
    ScanParentsResult,
    ServiceDiscoveryPreviewResult,
    ServiceDiscoveryResult,
    ServiceInfo,
    SetAutochecksInput,
    SetAutochecksV2Result,
    SpecialAgentResult,
    UpdateDNSCacheResult,
    UpdateHostLabelsResult,
    UpdatePasswordsMergedFileResult,
)

from cmk.snmplib import (
    BackendOIDSpec,
    BackendSNMPTree,
    get_snmp_table,
    oids_to_walk,
    SNMPCredentials,
    SNMPHostConfig,
    SNMPVersion,
    walk_for_export,
)

from cmk.fetchers import get_raw_data, Mode, ProgramFetcher, SNMPScanConfig, TCPFetcher, TLSConfig
from cmk.fetchers.config import make_persisted_section_dir
from cmk.fetchers.filecache import FileCacheOptions, MaxAge
from cmk.fetchers.snmp import make_backend as make_snmp_backend

from cmk.checkengine.checking import CheckPluginName, ServiceConfigurer
from cmk.checkengine.discovery import (
    AutocheckEntry,
    autodiscovery,
    automation_discovery,
    CheckPreview,
    CheckPreviewEntry,
    DiscoveryMode,
    DiscoveryResult,
    DiscoverySettings,
    get_check_preview,
    set_autochecks_for_effective_host,
)
from cmk.checkengine.fetcher import FetcherFunction, FetcherType, SourceType
from cmk.checkengine.parameters import TimespecificParameters
from cmk.checkengine.parser import NO_SELECTION, parse_raw_data
from cmk.checkengine.submitters import ServiceDetails, ServiceState
from cmk.checkengine.summarize import summarize

import cmk.base.api.agent_based.register as agent_based_register
import cmk.base.core
import cmk.base.nagios_utils
import cmk.base.parent_scan
from cmk.base import config, core_config, notify, sources
from cmk.base.api.agent_based.plugin_classes import AgentBasedPlugins, CheckPlugin
from cmk.base.api.agent_based.value_store import ValueStoreManager
from cmk.base.automations import (
    Automation,
    automations,
    load_config,
    load_plugins,
    MKAutomationError,
)
from cmk.base.checkers import (
    CheckPluginMapper,
    CMKFetcher,
    CMKParser,
    CMKSummarizer,
    DiscoveryPluginMapper,
    HostLabelPluginMapper,
    SectionPluginMapper,
    SpecialAgentFetcher,
)
from cmk.base.config import (
    ConfigCache,
    ConfiguredIPLookup,
    handle_ip_lookup_failure,
    lookup_mgmt_board_ip_address,
    snmp_default_community,
)
from cmk.base.core import CoreAction, do_restart
from cmk.base.core_factory import create_core
from cmk.base.diagnostics import DiagnosticsDump
from cmk.base.errorhandling import create_section_crash_dump
from cmk.base.parent_scan import ScanConfig
from cmk.base.sources import make_parser, SNMPFetcherConfig

from cmk.agent_based.v1.value_store import set_value_store_manager
from cmk.discover_plugins import discover_families, PluginGroup
from cmk.piggyback.backend import move_for_host_rename as move_piggyback_for_host_rename
from cmk.server_side_calls_backend import (
    ExecutableFinder,
    load_special_agents,
    SpecialAgent,
    SpecialAgentCommandLine,
)

HistoryFile = str
HistoryFilePair = tuple[HistoryFile, HistoryFile]


def _schedule_discovery_check(host_name: HostName) -> None:
    now = int(time.time())
    service = (
        "Check_MK Discovery"
        if "cmk_inventory" in config.use_new_descriptions_for
        else "Check_MK inventory"
    )
    # Ignore missing check and avoid warning in cmc.log
    cmc_try = ";TRY" if config.monitoring_core == "cmc" else ""
    command = f"SCHEDULE_FORCED_SVC_CHECK;{host_name};{service};{now}{cmc_try}"

    try:
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.connect(cmk.utils.paths.livestatus_unix_socket)
        s.send(f"COMMAND [{now}] {command}\n".encode())
    except Exception:
        if cmk.ccc.debug.enabled():
            raise


class DiscoveryAutomation(Automation):
    def _trigger_discovery_check(self, config_cache: ConfigCache, host_name: HostName) -> None:
        """if required, schedule the "Check_MK Discovery" check"""
        if not config.inventory_check_autotrigger:
            return

        if config_cache.discovery_check_parameters(host_name).commandline_only:
            return

        if host_name in config_cache.hosts_config.clusters:
            return

        _schedule_discovery_check(host_name)


def _extract_directive(directive: str, args: list[str]) -> tuple[bool, list[str]]:
    if directive in args:
        return True, [a for i, a in enumerate(args) if i != args.index(directive)]
    return False, args


class AutomationDiscovery(DiscoveryAutomation):
    cmd = "service-discovery"

    # Does discovery for a list of hosts. For possible values see
    # DiscoverySettings
    # Hosts on the list that are offline (unmonitored) will
    # be skipped.
    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> ServiceDiscoveryResult:
        force_snmp_cache_refresh, args = _extract_directive("@scan", args)
        _prevent_scan, args = _extract_directive("@noscan", args)
        raise_errors, args = _extract_directive("@raiseerrors", args)
        # Error sensitivity
        if raise_errors:
            on_error = OnError.RAISE
            os.dup2(os.open("/dev/null", os.O_WRONLY), 2)
        else:
            on_error = OnError.IGNORE

        # `force_snmp_cache_refresh` overrides `use_outdated` for SNMP.
        file_cache_options = FileCacheOptions(use_outdated=True)

        if len(args) < 2:
            raise MKAutomationError(
                "Need two arguments: %s " % "DiscoveryMode|DiscoverySettings HOSTNAME"
            )

        # TODO 2.3 introduced a new format but has to be compatible for 2.2.
        # Can be removed one day
        if (discovery_settings := args[0]) in ["new", "remove", "fixall", "refresh"]:
            settings = DiscoverySettings.from_discovery_mode(
                DiscoveryMode.from_str(discovery_settings)
            )
        else:
            # 2.3 format
            settings = DiscoverySettings.from_json(discovery_settings)

        hostnames = [HostName(h) for h in islice(args, 1, None)]

        if plugins is None:
            plugins = load_plugins()

        if loading_result is None:
            loading_result = load_config(
                discovery_rulesets=agent_based_register.extract_known_discovery_rulesets(plugins)
            )

        discovery_config = config.DiscoveryConfigurer(
            loading_result.config_cache.ruleset_matcher,
            loading_result.loaded_config.discovery_rules,
        )
        config_cache = loading_result.config_cache
        ruleset_matcher = config_cache.ruleset_matcher
        autochecks_config = config.AutochecksConfigurer(config_cache, plugins.check_plugins)
        service_configurer = config_cache.make_service_configurer(plugins.check_plugins)

        results: dict[HostName, DiscoveryResult] = {}

        parser = CMKParser(
            config_cache.parser_factory(),
            selected_sections=NO_SELECTION,
            keep_outdated=file_cache_options.keep_outdated,
            logger=logging.getLogger("cmk.base.discovery"),
        )
        fetcher = CMKFetcher(
            config_cache,
            config_cache.fetcher_factory(service_configurer),
            plugins,
            file_cache_options=file_cache_options,
            force_snmp_cache_refresh=force_snmp_cache_refresh,
            ip_address_of=config.ConfiguredIPLookup(
                config_cache, error_handler=config.handle_ip_lookup_failure
            ),
            mode=Mode.DISCOVERY,
            on_error=on_error,
            selected_sections=NO_SELECTION,
            simulation_mode=config.simulation_mode,
            snmp_backend_override=None,
            password_store_file=cmk.utils.password_store.pending_password_store_path(),
        )
        for hostname in hostnames:

            def section_error_handling(
                section_name: SectionName,
                raw_data: Sequence[object],
                host_name: HostName = hostname,
            ) -> str:
                return create_section_crash_dump(
                    operation="parsing",
                    section_name=section_name,
                    section_content=raw_data,
                    host_name=host_name,
                    rtc_package=None,
                )

            hosts_config = config_cache.hosts_config
            results[hostname] = automation_discovery(
                hostname,
                is_cluster=hostname in config_cache.hosts_config.clusters,
                cluster_nodes=config_cache.nodes(hostname),
                active_hosts={
                    hn
                    for hn in itertools.chain(hosts_config.hosts, hosts_config.clusters)
                    if config_cache.is_active(hn) and config_cache.is_online(hn)
                },
                ruleset_matcher=ruleset_matcher,
                parser=parser,
                fetcher=fetcher,
                summarizer=CMKSummarizer(
                    hostname,
                    config_cache.summary_config,
                    override_non_ok_state=None,
                ),
                section_plugins=SectionPluginMapper(
                    {**plugins.agent_sections, **plugins.snmp_sections}
                ),
                section_error_handling=section_error_handling,
                host_label_plugins=HostLabelPluginMapper(
                    config_getter=discovery_config,
                    sections={**plugins.agent_sections, **plugins.snmp_sections},
                ),
                plugins=DiscoveryPluginMapper(
                    config_getter=discovery_config,
                    check_plugins=plugins.check_plugins,
                ),
                autochecks_config=autochecks_config,
                settings=settings,
                keep_clustered_vanished_services=True,
                service_filters=None,
                enforced_services=config_cache.enforced_services_table(
                    hostname, plugins.check_plugins
                ),
                on_error=on_error,
            )

            if results[hostname].error_text is None:
                # Trigger the discovery service right after performing the discovery to
                # make the service reflect the new state as soon as possible.
                self._trigger_discovery_check(config_cache, hostname)

        return ServiceDiscoveryResult(results)


automations.register(AutomationDiscovery())


class AutomationDiscoveryPre22Name(AutomationDiscovery):
    cmd = "inventory"


automations.register(AutomationDiscoveryPre22Name())


class AutomationSpecialAgentDiscoveryPreview(Automation):
    cmd = "special-agent-discovery-preview"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> ServiceDiscoveryPreviewResult:
        run_settings = DiagSpecialAgentInput.deserialize(sys.stdin.read())

        if plugins is None:
            plugins = load_plugins()
        if loading_result is None:
            loading_result = load_config(
                discovery_rulesets=agent_based_register.extract_known_discovery_rulesets(plugins)
            )

        config_cache = loading_result.config_cache
        service_configurer = config_cache.make_service_configurer(plugins.check_plugins)
        file_cache_options = FileCacheOptions(use_outdated=False, use_only_cache=False)
        password_store_file = Path(cmk.utils.paths.tmp_dir, f"passwords_temp_{uuid.uuid4()}")
        try:
            cmk.utils.password_store.save(run_settings.passwords, password_store_file)
            cmds = get_special_agent_commandline(
                run_settings.host_config,
                run_settings.agent_name,
                run_settings.params,
                password_store_file,
                run_settings.passwords,
                run_settings.http_proxies,
            )
            fetcher = SpecialAgentFetcher(
                config_cache.fetcher_factory(service_configurer),
                agent_name=run_settings.agent_name,
                cmds=cmds,
                file_cache_options=file_cache_options,
            )
            preview = _get_discovery_preview(
                run_settings.host_config.host_name,
                OnError.RAISE,
                fetcher,
                file_cache_options,
                loading_result.loaded_config,
                config_cache,
                plugins,
                ip_address_of_host,
                run_settings.host_config.ip_address,
            )
        finally:
            if password_store_file.exists():
                password_store_file.unlink()
        return preview


automations.register(AutomationSpecialAgentDiscoveryPreview())


class AutomationDiscoveryPreview(Automation):
    cmd = "service-discovery-preview"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> ServiceDiscoveryPreviewResult:
        prevent_fetching, args = _extract_directive("@nofetch", args)
        raise_errors, args = _extract_directive("@raiseerrors", args)
        host_name = HostName(args[0])

        if plugins is None:
            plugins = load_plugins()
        if loading_result is None:
            loading_result = load_config(
                discovery_rulesets=agent_based_register.extract_known_discovery_rulesets(plugins)
            )

        config_cache = loading_result.config_cache
        config_cache.ruleset_matcher.ruleset_optimizer.set_all_processed_hosts({host_name})
        service_configurer = config_cache.make_service_configurer(plugins.check_plugins)
        on_error = OnError.RAISE if raise_errors else OnError.WARN
        file_cache_options = FileCacheOptions(
            use_outdated=prevent_fetching, use_only_cache=prevent_fetching
        )
        fetcher = CMKFetcher(
            config_cache,
            config_cache.fetcher_factory(service_configurer),
            plugins,
            file_cache_options=file_cache_options,
            force_snmp_cache_refresh=not prevent_fetching,
            ip_address_of=config.ConfiguredIPLookup(
                config_cache, error_handler=config.handle_ip_lookup_failure
            ),
            mode=Mode.DISCOVERY,
            on_error=on_error,
            selected_sections=NO_SELECTION,
            simulation_mode=config.simulation_mode,
            snmp_backend_override=None,
            password_store_file=cmk.utils.password_store.pending_password_store_path(),
        )
        ip_address_of = config.ConfiguredIPLookup(
            config_cache, error_handler=config.handle_ip_lookup_failure
        )
        hosts_config = config.make_hosts_config()
        ip_address = (
            None
            if host_name in hosts_config.clusters
            or ConfigCache.ip_stack_config(host_name) is ip_lookup.IPStackConfig.NO_IP
            # We *must* do the lookup *before* calling `get_host_attributes()`
            # because...  I don't know... global variables I guess.  In any case,
            # doing it the other way around breaks one integration test.
            # note (mo): The baviour of repeated lookups changed. The above _might_ not be true anymore.
            else config.lookup_ip_address(config_cache, host_name)
        )
        return _get_discovery_preview(
            host_name,
            on_error,
            fetcher,
            file_cache_options,
            loading_result.loaded_config,
            config_cache,
            plugins,
            ip_address_of,
            ip_address,
        )


automations.register(AutomationDiscoveryPreview())


def _get_discovery_preview(
    host_name: HostName,
    on_error: OnError,
    fetcher: FetcherFunction,
    file_cache_options: FileCacheOptions,
    loaded_config: config.LoadedConfigFragment,
    config_cache: config.ConfigCache,
    plugins: AgentBasedPlugins,
    ip_address_of: config.IPLookup,
    ip_address: HostAddress | None,
) -> ServiceDiscoveryPreviewResult:
    buf = io.StringIO()

    with redirect_stdout(buf), redirect_stderr(buf):
        log.setup_console_logging()

        check_preview = _execute_discovery(
            host_name,
            on_error,
            ip_address_of,
            ip_address,
            fetcher,
            file_cache_options,
            loaded_config,
            config_cache,
            plugins=plugins,
        )

        def make_discovered_host_labels(
            labels: Sequence[HostLabel],
        ) -> DiscoveredHostLabelsDict:
            # this dict deduplicates label names! TODO: sort only if and where needed!
            return {l.name: l.to_dict() for l in sorted(labels, key=operator.attrgetter("name"))}

        changed_labels = make_discovered_host_labels(
            [
                l
                for l in check_preview.labels.vanished
                if l.name in make_discovered_host_labels(check_preview.labels.new)
            ]
        )

        return ServiceDiscoveryPreviewResult(
            output=buf.getvalue(),
            check_table=check_preview.table[host_name],
            nodes_check_table={h: t for h, t in check_preview.table.items() if h != host_name},
            host_labels=make_discovered_host_labels(check_preview.labels.present),
            new_labels=make_discovered_host_labels(
                [l for l in check_preview.labels.new if l.name not in changed_labels]
            ),
            vanished_labels=make_discovered_host_labels(
                [l for l in check_preview.labels.vanished if l.name not in changed_labels]
            ),
            changed_labels=changed_labels,
            source_results={
                k: (r.state, r.as_text()) for k, r in check_preview.source_results.items()
            },
            labels_by_host=check_preview.kept_labels,
        )


def _active_check_preview_rows(
    config_cache: ConfigCache,
    host_name: HostName,
    ip_address_of: config.IPLookup,
) -> Sequence[CheckPreviewEntry]:
    ignored_services = config.IgnoredActiveServices(config_cache, host_name)

    def make_check_source(desc: str) -> str:
        return "ignored_active" if desc in ignored_services else "active"

    def make_output(desc: str) -> str:
        pretty = make_check_source(desc).rsplit("_", maxsplit=1)[-1].title()
        return f"WAITING - {pretty} check, cannot be done offline"

    password_store_file = cmk.utils.password_store.pending_password_store_path()

    return [
        CheckPreviewEntry(
            check_source=make_check_source(active_service.description),
            check_plugin_name=active_service.plugin_name,
            ruleset_name=None,
            discovery_ruleset_name=None,
            item=active_service.description,
            old_discovered_parameters={},
            new_discovered_parameters={},
            effective_parameters=active_service.configuration,
            description=active_service.description,
            state=None,
            output=make_output(active_service.description),
            metrics=[],
            old_labels={},
            new_labels={},
            found_on_nodes=[host_name],
        )
        for active_service in config_cache.active_check_services(
            host_name,
            config_cache.get_host_attributes(host_name, ip_address_of),
            ip_address_of,
            cmk.utils.password_store.load(password_store_file),
            password_store_file,
        )
    ]


def _make_compute_check_parameters_of_autocheck(
    ruleset_matcher: RulesetMatcher,
    check_plugins: Mapping[CheckPluginName, CheckPlugin],
    parameter_rules: Mapping[str, Sequence[RuleSpec[Mapping[str, object]]]],
) -> Callable[[HostName, AutocheckEntry], TimespecificParameters]:
    def compute_check_parameters_of_autocheck(
        host_name: HostName, entry: AutocheckEntry
    ) -> TimespecificParameters:
        service_name = config.service_description(
            ruleset_matcher,
            host_name,
            entry.check_plugin_name,
            service_name_template=(
                None
                if (
                    p := agent_based_register.get_check_plugin(
                        entry.check_plugin_name, check_plugins
                    )
                )
                is None
                else p.service_name
            ),
            item=entry.item,
        )
        return config.compute_check_parameters(
            ruleset_matcher,
            check_plugins,
            host_name,
            entry.check_plugin_name,
            entry.item,
            ruleset_matcher.labels_of_service(host_name, service_name, entry.service_labels),
            entry.parameters,
            parameter_rules,
        )

    return compute_check_parameters_of_autocheck


def _execute_discovery(
    host_name: HostName,
    on_error: OnError,
    ip_address_of: config.IPLookup,
    ip_address: HostAddress | None,
    fetcher: FetcherFunction,
    file_cache_options: FileCacheOptions,
    loaded_config: config.LoadedConfigFragment,
    config_cache: config.ConfigCache,
    plugins: AgentBasedPlugins,
) -> CheckPreview:
    hosts_config = config.make_hosts_config()
    discovery_config = config.DiscoveryConfigurer(
        config_cache.ruleset_matcher,
        loaded_config.discovery_rules,
    )
    ruleset_matcher = config_cache.ruleset_matcher
    autochecks_config = config.AutochecksConfigurer(config_cache, plugins.check_plugins)
    parser = CMKParser(
        config_cache.parser_factory(),
        selected_sections=NO_SELECTION,
        keep_outdated=file_cache_options.keep_outdated,
        logger=logging.getLogger("cmk.base.discovery"),
    )

    with (
        set_value_store_manager(
            ValueStoreManager(host_name), store_changes=False
        ) as value_store_manager,
    ):
        is_cluster = host_name in hosts_config.clusters
        check_plugins = CheckPluginMapper(
            config_cache,
            plugins.check_plugins,
            value_store_manager,
            clusters=hosts_config.clusters,
            rtc_package=None,
        )
        passive_check_preview = get_check_preview(
            host_name,
            ip_address,
            is_cluster=is_cluster,
            cluster_nodes=config_cache.nodes(host_name),
            parser=parser,
            fetcher=fetcher,
            summarizer=CMKSummarizer(
                host_name,
                config_cache.summary_config,
                override_non_ok_state=None,
            ),
            section_plugins=SectionPluginMapper(
                {**plugins.agent_sections, **plugins.snmp_sections}
            ),
            section_error_handling=lambda section_name, raw_data: create_section_crash_dump(
                operation="parsing",
                section_name=section_name,
                section_content=raw_data,
                host_name=host_name,
                rtc_package=None,
            ),
            host_label_plugins=HostLabelPluginMapper(
                config_getter=discovery_config,
                sections={**plugins.agent_sections, **plugins.snmp_sections},
            ),
            check_plugins=check_plugins,
            compute_check_parameters=_make_compute_check_parameters_of_autocheck(
                ruleset_matcher, plugins.check_plugins, loaded_config.checkgroup_parameters
            ),
            discovery_plugins=DiscoveryPluginMapper(
                config_getter=discovery_config,
                check_plugins=plugins.check_plugins,
            ),
            autochecks_config=autochecks_config,
            enforced_services=config_cache.enforced_services_table(
                host_name, plugins=plugins.check_plugins
            ),
            on_error=on_error,
        )
    return CheckPreview(
        table={
            h: [
                *table,
                *_active_check_preview_rows(config_cache, h, ip_address_of),
                *config_cache.custom_check_preview_rows(h),
            ]
            for h, table in passive_check_preview.table.items()
        },
        labels=passive_check_preview.labels,
        source_results=passive_check_preview.source_results,
        kept_labels=passive_check_preview.kept_labels,
    )


class AutomationAutodiscovery(DiscoveryAutomation):
    cmd = "autodiscovery"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> AutodiscoveryResult:
        with redirect_stdout(open(os.devnull, "w")):
            result = _execute_autodiscovery(plugins, loading_result)

        return AutodiscoveryResult(*result)


automations.register(AutomationAutodiscovery())


def _execute_autodiscovery(
    ab_plugins: AgentBasedPlugins | None,
    loading_result: config.LoadingResult | None,
) -> tuple[Mapping[HostName, DiscoveryResult], bool]:
    file_cache_options = FileCacheOptions(use_outdated=True)

    if not (autodiscovery_queue := AutoQueue(autodiscovery_dir)):
        return {}, False

    ab_plugins = load_plugins() if ab_plugins is None else ab_plugins
    if loading_result is None:
        loading_result = load_config(
            discovery_rulesets=agent_based_register.extract_known_discovery_rulesets(ab_plugins)
        )

    config_cache = loading_result.config_cache
    service_configurer = config_cache.make_service_configurer(ab_plugins.check_plugins)
    discovery_config = config.DiscoveryConfigurer(
        config_cache.ruleset_matcher, loading_result.loaded_config.discovery_rules
    )
    autochecks_config = config.AutochecksConfigurer(config_cache, ab_plugins.check_plugins)
    ip_address_of = config.ConfiguredIPLookup(
        config_cache,
        # error handling: we're redirecting stdout to /dev/null anyway,
        # and not using the collected errors.
        # However: Currently the config creation expects an IPLookup that
        # allows to access the lookup faiures.
        error_handler=ip_lookup.CollectFailedHosts(),
    )
    ruleset_matcher = config_cache.ruleset_matcher
    parser = CMKParser(
        config_cache.parser_factory(),
        selected_sections=NO_SELECTION,
        keep_outdated=file_cache_options.keep_outdated,
        logger=logging.getLogger("cmk.base.discovery"),
    )
    fetcher = CMKFetcher(
        config_cache,
        config_cache.fetcher_factory(service_configurer),
        ab_plugins,
        file_cache_options=file_cache_options,
        force_snmp_cache_refresh=False,
        ip_address_of=config.ConfiguredIPLookup(
            config_cache, error_handler=config.handle_ip_lookup_failure
        ),
        mode=Mode.DISCOVERY,
        on_error=OnError.IGNORE,
        selected_sections=NO_SELECTION,
        simulation_mode=config.simulation_mode,
        snmp_backend_override=None,
        password_store_file=cmk.utils.password_store.core_password_store_path(LATEST_CONFIG),
    )
    section_plugins = SectionPluginMapper({**ab_plugins.agent_sections, **ab_plugins.snmp_sections})
    host_label_plugins = HostLabelPluginMapper(
        config_getter=discovery_config,
        sections={**ab_plugins.agent_sections, **ab_plugins.snmp_sections},
    )
    plugins = DiscoveryPluginMapper(
        config_getter=discovery_config,
        check_plugins=ab_plugins.check_plugins,
    )
    on_error = OnError.IGNORE

    hosts_config = config_cache.hosts_config
    all_hosts = frozenset(
        itertools.chain(hosts_config.hosts, hosts_config.clusters, hosts_config.shadow_hosts)
    )
    for host_name in autodiscovery_queue:
        if host_name not in all_hosts:
            console.verbose(f"  Removing mark '{host_name}' (host not configured")
            (autodiscovery_queue.path / str(host_name)).unlink(missing_ok=True)

    if (oldest_queued := autodiscovery_queue.oldest()) is None:
        console.verbose("Autodiscovery: No hosts marked by discovery check")
        return {}, False

    console.verbose("Autodiscovery: Discovering all hosts marked by discovery check:")
    try:
        response = livestatus.LocalConnection().query("GET hosts\nColumns: name state")
        process_hosts: Container[HostName] = {
            HostName(name) for name, state in response if state == 0
        }
    except (livestatus.MKLivestatusNotFoundError, livestatus.MKLivestatusSocketError):
        process_hosts = EVERYTHING

    activation_required = False
    rediscovery_reference_time = time.time()

    hosts_processed = set()
    discovery_results = {}

    start = time.monotonic()
    limit = 120
    message = f"  Timeout of {limit} seconds reached. Let's do the remaining hosts next time."

    try:
        with Timeout(limit + 10, message=message):
            for host_name in autodiscovery_queue:
                if time.monotonic() > start + limit:
                    raise TimeoutError(message)

                if host_name not in process_hosts:
                    continue

                def section_error_handling(
                    section_name: SectionName,
                    raw_data: Sequence[object],
                    host_name: HostName = host_name,
                ) -> str:
                    return create_section_crash_dump(
                        operation="parsing",
                        section_name=section_name,
                        section_content=raw_data,
                        host_name=host_name,
                        rtc_package=None,
                    )

                hosts_processed.add(host_name)
                console.verbose(f"{tty.bold}{host_name}{tty.normal}:")
                params = config_cache.discovery_check_parameters(host_name)
                if params.commandline_only:
                    console.verbose("  failed: discovery check disabled")
                    discovery_result, activate_host = None, False
                else:
                    hosts_config = config_cache.hosts_config
                    discovery_result, activate_host = autodiscovery(
                        host_name,
                        is_cluster=host_name in config_cache.hosts_config.clusters,
                        cluster_nodes=config_cache.nodes(host_name),
                        active_hosts={
                            hn
                            for hn in itertools.chain(hosts_config.hosts, hosts_config.clusters)
                            if config_cache.is_active(hn) and config_cache.is_online(hn)
                        },
                        ruleset_matcher=ruleset_matcher,
                        parser=parser,
                        fetcher=fetcher,
                        summarizer=CMKSummarizer(
                            host_name,
                            config_cache.summary_config,
                            override_non_ok_state=None,
                        ),
                        section_plugins=section_plugins,
                        section_error_handling=section_error_handling,
                        host_label_plugins=host_label_plugins,
                        plugins=plugins,
                        autochecks_config=autochecks_config,
                        schedule_discovery_check=_schedule_discovery_check,
                        rediscovery_parameters=params.rediscovery,
                        invalidate_host_config=config_cache.invalidate_host_config,
                        autodiscovery_queue=autodiscovery_queue,
                        reference_time=rediscovery_reference_time,
                        oldest_queued=oldest_queued,
                        enforced_services=config_cache.enforced_services_table(
                            host_name, ab_plugins.check_plugins
                        ),
                        on_error=on_error,
                    )
                if discovery_result:
                    discovery_results[host_name] = discovery_result
                    activation_required |= activate_host

    except (MKTimeout, TimeoutError) as exc:
        console.verbose_no_lf(str(exc))

    if not activation_required:
        return discovery_results, False

    core = create_core(config.monitoring_core)
    with config.set_use_core_config(
        autochecks_dir=Path(base_autochecks_dir),
        discovered_host_labels_dir=base_discovered_host_labels_dir,
    ):
        try:
            cache_manager.clear_all()
            config_cache.initialize()
            hosts_config = config.make_hosts_config()

            # reset these to their original value to create a correct config
            if config.monitoring_core == "cmc":
                cmk.base.core.do_reload(
                    config_cache,
                    ip_address_of,
                    core,
                    ab_plugins,
                    locking_mode=config.restart_locking,
                    all_hosts=hosts_config.hosts,
                    discovery_rules=loading_result.loaded_config.discovery_rules,
                    duplicates=sorted(
                        hosts_config.duplicates(
                            lambda hn: config_cache.is_active(hn) and config_cache.is_online(hn)
                        ),
                    ),
                )
            else:
                cmk.base.core.do_restart(
                    config_cache,
                    ip_address_of,
                    core,
                    ab_plugins,
                    all_hosts=hosts_config.hosts,
                    locking_mode=config.restart_locking,
                    discovery_rules=loading_result.loaded_config.discovery_rules,
                    duplicates=sorted(
                        hosts_config.duplicates(
                            lambda hn: config_cache.is_active(hn) and config_cache.is_online(hn)
                        ),
                    ),
                )
        finally:
            cache_manager.clear_all()
            config_cache.initialize()

    return discovery_results, True


def _make_get_effective_host_of_autocheck_callback(
    config_cache: ConfigCache,
    check_plugins: Mapping[CheckPluginName, CheckPlugin],
    precomputed_service_descriptions: Mapping[tuple[HostName, CheckPluginName, Item], ServiceName],
) -> Callable[[HostName, AutocheckEntry], HostName]:
    def get_effective_host_of_autocheck(host: HostName, entry: AutocheckEntry) -> HostName:
        service_name = precomputed_service_descriptions.get(
            (host, entry.check_plugin_name, entry.item)
        ) or config.service_description(
            config_cache.ruleset_matcher,
            host,
            entry.check_plugin_name,
            service_name_template=(
                None
                if (
                    p := agent_based_register.get_check_plugin(
                        entry.check_plugin_name, check_plugins
                    )
                )
                is None
                else p.service_name
            ),
            item=entry.item,
        )
        return config_cache.effective_host(
            host,
            service_name,
            config_cache.ruleset_matcher.labels_of_service(
                host, service_name, entry.service_labels
            ),
        )

    return get_effective_host_of_autocheck


class AutomationSetAutochecksV2(DiscoveryAutomation):
    cmd = "set-autochecks-v2"
    # This is an incompatibly changed version of the set-autochecks command.
    # The last version to support the old 'set-autochecks' was 2.4
    # Consider changing the name back to 'set-autochecks' in 2.6

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> SetAutochecksV2Result:
        set_autochecks_input = SetAutochecksInput.deserialize(sys.stdin.read())

        if plugins is None:
            plugins = load_plugins()

        check_plugins = plugins.check_plugins
        if loading_result is None:
            loading_result = load_config(
                discovery_rulesets=agent_based_register.extract_known_discovery_rulesets(plugins)
            )
        config_cache = loading_result.config_cache

        service_descriptions: Mapping[tuple[HostName, CheckPluginName, str | None], ServiceName] = {
            (host, autocheck_entry.check_plugin_name, autocheck_entry.item): service_name
            for host, services in {
                **{set_autochecks_input.discovered_host: set_autochecks_input.target_services},
                **set_autochecks_input.nodes_services,
            }.items()
            for service_name, autocheck_entry in services.items()
        }

        # This function is used to get the effective host for a service description.
        # Some of the service_descriptions are actually already passed down in which case they
        # are used directly. In case all service_descriptions are passed down, needs_checks can
        # be set to False.
        get_effective_host_of_autocheck = _make_get_effective_host_of_autocheck_callback(
            config_cache, check_plugins, service_descriptions
        )

        if set_autochecks_input.discovered_host not in config_cache.hosts_config.clusters:
            set_autochecks_for_effective_host(
                autochecks_owner=set_autochecks_input.discovered_host,
                effective_host=set_autochecks_input.discovered_host,
                new_services=set_autochecks_input.target_services.values(),
                get_effective_host=get_effective_host_of_autocheck,
            )
        else:
            desired_on_cluster = {s.id() for s in set_autochecks_input.target_services.values()}
            for node, services in set_autochecks_input.nodes_services.items():
                set_autochecks_for_effective_host(
                    autochecks_owner=node,
                    effective_host=set_autochecks_input.discovered_host,
                    new_services=(s for s in services.values() if s.id() in desired_on_cluster),
                    get_effective_host=get_effective_host_of_autocheck,
                )

        self._trigger_discovery_check(config_cache, set_autochecks_input.discovered_host)

        return SetAutochecksV2Result()


automations.register(AutomationSetAutochecksV2())


class AutomationUpdateHostLabels(DiscoveryAutomation):
    """Set the new collection of discovered host labels"""

    cmd = "update-host-labels"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> UpdateHostLabelsResult:
        hostname = HostName(args[0])
        DiscoveredHostLabelsStore(hostname).save(
            [
                HostLabel.from_dict(name, hl_dict)
                for name, hl_dict in ast.literal_eval(sys.stdin.read()).items()
            ]
        )

        if loading_result is None:
            loading_result = load_config(discovery_rulesets=())
        self._trigger_discovery_check(loading_result.config_cache, hostname)
        return UpdateHostLabelsResult()


automations.register(AutomationUpdateHostLabels())


class AutomationRenameHosts(Automation):
    cmd = "rename-hosts"

    def __init__(self) -> None:
        super().__init__()
        self._finished_history_files: dict[HistoryFilePair, list[HistoryFile]] = {}

    # WATO calls this automation when hosts have been renamed. We need to change
    # several file and directory names. This function has no argument but reads
    # Python pair-list from stdin:
    # [("old1", "new1"), ("old2", "new2")])
    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> RenameHostsResult:
        renamings: list[HistoryFilePair] = ast.literal_eval(sys.stdin.read())

        if plugins is None:
            plugins = load_plugins()
        if loading_result is None:
            loading_result = load_config(
                discovery_rulesets=agent_based_register.extract_known_discovery_rulesets(plugins)
            )

        actions: list[str] = []

        # The history archive can be renamed with running core. We need to keep
        # the list of already handled history archive files, because a new history
        # file may be created by the core during this step. All unhandled files,
        # including the current history files will be handled later when the core
        # is stopped.
        for oldname, newname in renamings:
            self._finished_history_files[(oldname, newname)] = (
                self._rename_host_in_core_history_archive(oldname, newname)
            )
            if self._finished_history_files[(oldname, newname)]:
                actions.append("history")

        # At this place WATO already has changed it's configuration. All further
        # data might be changed by the still running core. So we need to stop
        # it now.
        core_was_running = self._core_is_running()
        if core_was_running:
            cmk.base.core.do_core_action(
                CoreAction.STOP,
                quiet=True,
                monitoring_core=config.monitoring_core,
            )

        try:
            for oldname, newname in renamings:
                actions += self._rename_host_files(oldname, newname)
        finally:
            # Start monitoring again
            if core_was_running:
                # force config generation to succeed. The core *must* start.
                # In this case the configuration is already locked by the caller of the automation.
                # If that is on the local site, we can not lock the configuration again during baking!
                # (If we are on a remote site now, locking *would* work, but we will not bake agents anyway.)
                config_cache = loading_result.config_cache
                hosts_config = config.make_hosts_config()
                ip_address_of = config.ConfiguredIPLookup(
                    config_cache, error_handler=ip_lookup.CollectFailedHosts()
                )
                _execute_silently(
                    config_cache,
                    CoreAction.START,
                    ip_address_of,
                    hosts_config,
                    loading_result.loaded_config,
                    plugins,
                    skip_config_locking_for_bakery=True,
                )

                for hostname in ip_address_of.error_handler.failed_ip_lookups:
                    actions.append("dnsfail-" + hostname)

        # Convert actions into a dictionary { "what" : count }
        action_counts: dict[str, int] = {}
        for action in actions:
            action_counts.setdefault(action, 0)
            action_counts[action] += 1

        return RenameHostsResult(action_counts)

    def _core_is_running(self) -> bool:
        if config.monitoring_core == "nagios":
            command = nagios_startscript + " status"
        else:
            command = "omd status cmc"
        return (
            subprocess.call(
                shlex.split(command),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            == 0
        )

    def _rename_host_files(
        self,
        oldname: HistoryFile,
        newname: HistoryFile,
    ) -> list[str]:
        actions = []

        if self._rename_host_file(autochecks_dir, oldname + ".mk", newname + ".mk"):
            actions.append("autochecks")

        if self._rename_host_file(
            str(discovered_host_labels_dir), oldname + ".mk", newname + ".mk"
        ):
            actions.append("host-labels")

        # Rename temporary files of the host
        for d in ["cache", "counters"]:
            if self._rename_host_file(str(tmp_dir / d), oldname, newname):
                actions.append(d)

        actions.extend(move_piggyback_for_host_rename(cmk.utils.paths.omd_root, oldname, newname))

        # Logwatch
        if self._rename_host_dir(logwatch_dir, oldname, newname):
            actions.append("logwatch")

        # SNMP walks
        if self._rename_host_file(snmpwalks_dir, oldname, newname):
            actions.append("snmpwalk")

        # HW/SW Inventory
        if self._rename_host_file(var_dir + "/inventory", oldname, newname):
            self._rename_host_file(var_dir + "/inventory", oldname + ".gz", newname + ".gz")
            actions.append("inv")

        if self._rename_host_dir(var_dir + "/inventory_archive", oldname, newname):
            actions.append("invarch")

        # Baked agents
        baked_agents_dir = var_dir + "/agents/"
        have_renamed_agent = False
        if os.path.exists(baked_agents_dir):
            for opsys in os.listdir(baked_agents_dir):
                if self._rename_host_file(baked_agents_dir + opsys, oldname, newname):
                    have_renamed_agent = True
        if have_renamed_agent:
            actions.append("agent")

        # Agent deployment
        deployment_dir = var_dir + "/agent_deployment/"
        if self._rename_host_file(deployment_dir, oldname, newname):
            actions.append("agent_deployment")

        actions += self._omd_rename_host(oldname, newname)

        return actions

    def _rename_host_dir(self, basedir: str, oldname: str, newname: str) -> int:
        if os.path.exists(basedir + "/" + oldname):
            if os.path.exists(basedir + "/" + newname):
                shutil.rmtree(basedir + "/" + newname)
            os.rename(basedir + "/" + oldname, basedir + "/" + newname)
            return 1
        return 0

    def _rename_host_file(self, basedir: str, oldname: str, newname: str) -> int:
        if os.path.exists(basedir + "/" + oldname):
            if os.path.exists(basedir + "/" + newname):
                os.remove(basedir + "/" + newname)
            os.rename(basedir + "/" + oldname, basedir + "/" + newname)
            return 1
        return 0

    # This functions could be moved out of Checkmk.
    def _omd_rename_host(
        self,
        oldname: str,
        newname: str,
    ) -> list[str]:
        oldregex = self._escape_name_for_regex_matching(oldname)
        actions = []

        # Temporarily stop processing of performance data
        npcd_running = (omd_root / "tmp/pnp4nagios/run/npcd.pid").exists()
        if npcd_running:
            os.system("omd stop npcd >/dev/null 2>&1 </dev/null")

        rrdcache_running = (omd_root / "tmp/run/rrdcached.sock").exists()
        if rrdcache_running:
            os.system("omd stop rrdcached >/dev/null 2>&1 </dev/null")

        try:
            # Fix pathnames in XML files
            self.rename_host_in_files(
                str(omd_root / "var/pnp4nagios/perfdata" / oldname / "*.xml"),
                "/perfdata/%s/" % oldregex,
                "/perfdata/%s/" % newname,
            )

            # RRD files
            if self._rename_host_dir(str(omd_root / "var/pnp4nagios/perfdata"), oldname, newname):
                actions.append("rrd")

            # RRD files
            if self._rename_host_dir(str(omd_root / "var/check_mk/rrd"), oldname, newname):
                actions.append("rrd")

            # entries of rrdcached journal
            if self.rename_host_in_files(
                str(omd_root / "var/rrdcached/rrd.journal.*"),
                "/(perfdata|rrd)/%s/" % oldregex,
                "/\\1/%s/" % newname,
                extended_regex=True,
            ):
                actions.append("rrdcached")

            # Spoolfiles of NPCD
            if self.rename_host_in_files(  #
                "%s/var/pnp4nagios/perfdata.dump" % omd_root,
                "HOSTNAME::%s    " % oldregex,  #
                "HOSTNAME::%s    " % newname,
            ) or self.rename_host_in_files(  #
                "%s/var/pnp4nagios/spool/perfdata.*" % omd_root,
                "HOSTNAME::%s    " % oldregex,  #
                "HOSTNAME::%s    " % newname,
            ):
                actions.append("pnpspool")
        finally:
            if rrdcache_running:
                os.system("omd start rrdcached >/dev/null 2>&1 </dev/null")

            if npcd_running:
                os.system("omd start npcd >/dev/null 2>&1 </dev/null")

        self._rename_host_in_remaining_core_history_files(oldname, newname)

        # State retention (important for Downtimes, Acknowledgements, etc.)
        if config.monitoring_core == "nagios":
            if self.rename_host_in_files(
                "%s/var/nagios/retention.dat" % omd_root,
                "^host_name=%s$" % oldregex,
                "host_name=%s" % newname,
                extended_regex=True,
            ):
                actions.append("retention")

        else:  # CMC
            # Create a file "renamed_hosts" with the information about the
            # renaming of the hosts. The core will honor this file when it
            # reads the status file with the saved state.
            Path(var_dir, "core/renamed_hosts").write_text(f"{oldname}\n{newname}\n")
            actions.append("retention")

        # NagVis maps
        if edition_supports_nagvis(version.edition(omd_root)) and self.rename_host_in_files(
            "%s/etc/nagvis/maps/*.cfg" % omd_root,
            "^[[:space:]]*host_name=%s[[:space:]]*$" % oldregex,
            "host_name=%s" % newname,
            extended_regex=True,
        ):
            actions.append("nagvis")

        return actions

    def _rename_host_in_remaining_core_history_files(self, oldname: str, newname: str) -> list[str]:
        """Perform the rename operation in all history archive files that have not been handled yet"""
        finished_file_paths = self._finished_history_files[(oldname, newname)]
        all_file_paths = set(self._get_core_history_files(only_archive=False))
        todo_file_paths = list(all_file_paths.difference(finished_file_paths))
        return self._rename_host_in_core_history_files(todo_file_paths, oldname, newname)

    def _rename_host_in_core_history_archive(self, oldname: str, newname: str) -> list[str]:
        """Perform the rename operation in all history archive files"""
        file_paths = self._get_core_history_files(only_archive=True)
        return self._rename_host_in_core_history_files(file_paths, oldname, newname)

    def _get_core_history_files(self, only_archive: bool) -> list[str]:
        path_patterns = [
            "var/check_mk/core/archive/*",
            "var/nagios/archive/*",
        ]

        if not only_archive:
            path_patterns += [
                "var/check_mk/core/history",
                "var/nagios/nagios.log",
            ]

        file_paths: list[str] = []
        for path_pattern in path_patterns:
            file_paths += glob.glob(f"{omd_root}/{path_pattern}")
        return file_paths

    def _rename_host_in_core_history_files(
        self, file_paths: list[str], oldname: str, newname: str
    ) -> list[str]:
        oldregex = self._escape_name_for_regex_matching(oldname)

        # Logfiles and history files of CMC and Nagios. Problem
        # here: the exact place of the hostname varies between the
        # various log entry lines
        sed_commands = rf"""
s/(INITIAL|CURRENT) (HOST|SERVICE) STATE: {oldregex};/\1 \2 STATE: {newname};/
s/(HOST|SERVICE) (DOWNTIME |FLAPPING |)ALERT: {oldregex};/\1 \2ALERT: {newname};/
s/PASSIVE (HOST|SERVICE) CHECK: {oldregex};/PASSIVE \1 CHECK: {newname};/
s/(HOST|SERVICE) NOTIFICATION: ([^;]+);{oldregex};/\1 NOTIFICATION: \2;{newname};/
"""

        handled_files: list[str] = []

        subprocess.run(
            ["sed", "-ri", "--file=/dev/fd/0", *file_paths],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            close_fds=True,
            input=sed_commands.encode("utf-8"),
            check=False,
        )
        # TODO: error handling?

        handled_files += file_paths

        return handled_files

    # Returns True in case files were found, otherwise False
    def rename_host_in_files(
        self, path_pattern: str, old: str, new: str, extended_regex: bool = False
    ) -> bool:
        matched_paths = glob.glob(path_pattern)
        if matched_paths:
            extended = ["-r"] if extended_regex else []
            subprocess.call(
                ["sed", "-i"] + extended + [f"s@{old}@{new}@"] + matched_paths,
                stderr=subprocess.DEVNULL,
            )
            return True

        return False

    def _escape_name_for_regex_matching(self, name: str) -> str:
        return name.replace(".", "[.]")


automations.register(AutomationRenameHosts())


class AutomationGetServicesLabels(Automation):
    cmd = "get-services-labels"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> GetServicesLabelsResult:
        host_name, services = HostName(args[0]), args[1:]

        if plugins is None:
            plugins = load_plugins()
        if loading_result is None:
            loading_result = load_config(
                discovery_rulesets=agent_based_register.extract_known_discovery_rulesets(plugins)
            )

        loading_result.config_cache.ruleset_matcher.ruleset_optimizer.set_all_processed_hosts(
            {host_name}
        )

        # I think we might be computing something here that the caller already knew.
        service_configurer = loading_result.config_cache.make_service_configurer(
            plugins.check_plugins
        )
        discovered_services = service_configurer.configure_autochecks(
            host_name, loading_result.config_cache.autochecks_manager.get_autochecks(host_name)
        )
        discovered_labels = {s.description: s.labels for s in discovered_services}

        return GetServicesLabelsResult(
            {
                service: loading_result.config_cache.ruleset_matcher.labels_of_service(
                    host_name, service, discovered_labels.get(service, {})
                )
                for service in services
            }
        )


automations.register(AutomationGetServicesLabels())


class AutomationGetServiceName(Automation):
    cmd = "get-service-name"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loaded_config: config.LoadingResult | None,
    ) -> GetServiceNameResult:
        if plugins is None:
            plugins = load_plugins()
        host_name, check_plugin_name, item = (
            HostName(args[0]),
            CheckPluginName(args[1]),
            ast.literal_eval(args[2]),
        )
        if loaded_config is None:
            loaded_config = load_config(
                discovery_rulesets=agent_based_register.extract_known_discovery_rulesets(plugins)
            )
        ruleset_matcher = loaded_config.config_cache.ruleset_matcher
        ruleset_matcher.ruleset_optimizer.set_all_processed_hosts({host_name})
        return GetServiceNameResult(
            config.service_description(
                ruleset_matcher,
                host_name,
                check_plugin_name,
                service_name_template=(
                    None
                    if (
                        p := agent_based_register.get_check_plugin(
                            check_plugin_name, plugins.check_plugins
                        )
                    )
                    is None
                    else p.service_name
                ),
                item=item,
            )
        )


automations.register(AutomationGetServiceName())


@dataclass
class _FoundService:
    service_info: ServiceInfo
    discovered_labels: Mapping[str, str]


class AutomationAnalyseServices(Automation):
    cmd = "analyse-service"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> AnalyseServiceResult:
        host_name = HostName(args[0])
        servicedesc = args[1]

        if plugins is None:
            plugins = load_plugins()
        if loading_result is None:
            loading_result = load_config(
                discovery_rulesets=agent_based_register.extract_known_discovery_rulesets(plugins)
            )
        loading_result.config_cache.ruleset_matcher.ruleset_optimizer.set_all_processed_hosts(
            {host_name}
        )

        return (
            AnalyseServiceResult(
                service_info=found.service_info,
                labels=loading_result.config_cache.ruleset_matcher.labels_of_service(
                    host_name, servicedesc, found.discovered_labels
                ),
                label_sources=loading_result.config_cache.ruleset_matcher.label_sources_of_service(
                    host_name, servicedesc, found.discovered_labels
                ),
            )
            if (
                found := self._search_service(
                    config_cache=loading_result.config_cache,
                    plugins=plugins,
                    host_name=host_name,
                    servicedesc=servicedesc,
                    ip_address_of=config.ConfiguredIPLookup(
                        loading_result.config_cache, error_handler=config.handle_ip_lookup_failure
                    ),
                    check_plugins=plugins.check_plugins,
                )
            )
            else AnalyseServiceResult(
                service_info={},
                labels={},
                label_sources={},
            )
        )

    def _search_service(
        self,
        config_cache: ConfigCache,
        plugins: AgentBasedPlugins,
        host_name: HostName,
        servicedesc: str,
        ip_address_of: config.IPLookup,
        check_plugins: Mapping[CheckPluginName, CheckPlugin],
    ) -> _FoundService | None:
        return next(
            chain(
                # special case. cheap to check, so check this first:
                self._search_checkmk_discovery_service(config_cache, host_name, servicedesc),
                self._search_enforced_checks(config_cache, host_name, servicedesc, check_plugins),
                self._search_discovered_checks(
                    config_cache,
                    host_name,
                    servicedesc,
                    plugins.check_plugins,
                ),
                self._search_classical_checks(config_cache, host_name, servicedesc),
                self._search_active_checks(config_cache, host_name, ip_address_of, servicedesc),
            ),
            None,
        )

    @staticmethod
    def _search_checkmk_discovery_service(
        config_cache: ConfigCache, host_name: HostName, servicedesc: str
    ) -> Iterable[_FoundService]:
        if servicedesc != "Check_MK Discovery":
            return
        yield _FoundService(
            service_info={
                "origin": "active",
                "checktype": "check-mk-inventory",
                "parameters": asdict(config_cache.discovery_check_parameters(host_name)),
            },
            discovered_labels={},
        )

    @staticmethod
    def _search_enforced_checks(
        config_cache: ConfigCache,
        host_name: HostName,
        servicedesc: str,
        check_plugins: Mapping[CheckPluginName, CheckPlugin],
    ) -> Iterable[_FoundService]:
        for checkgroup_name, service in config_cache.enforced_services_table(
            host_name, check_plugins
        ).values():
            if service.description == servicedesc:
                yield _FoundService(
                    service_info={
                        "origin": "static",  # TODO: (how) can we change this to "enforced"?
                        "checkgroup": checkgroup_name,
                        "checktype": str(service.check_plugin_name),
                        "item": service.item,
                        "parameters": service.parameters.preview(timeperiod_active),
                    },
                    discovered_labels=service.discovered_labels,
                )
                return

    @staticmethod
    def _search_discovered_checks(
        config_cache: ConfigCache,
        host_name: HostName,
        servicedesc: str,
        check_plugins: Mapping[CheckPluginName, CheckPlugin],
    ) -> Iterable[_FoundService]:
        # NOTE: Iterating over the check table would make things easier. But we might end up with
        # different information.
        service_configurer = config_cache.make_service_configurer(check_plugins)
        table = config_cache.check_table(host_name, check_plugins, service_configurer)
        services = (
            [
                service
                for node in config_cache.nodes(host_name)
                for service in service_configurer.configure_autochecks(
                    node, config_cache.autochecks_manager.get_autochecks(node)
                )
                if host_name
                == config_cache.effective_host(node, service.description, service.labels)
            ]
            if host_name in config_cache.hosts_config.clusters
            else service_configurer.configure_autochecks(
                host_name, config_cache.autochecks_manager.get_autochecks(host_name)
            )
        )

        for service in services:
            if service.id() not in table:
                continue  # this is a clustered service

            if service.description != servicedesc:
                continue

            plugin = agent_based_register.get_check_plugin(service.check_plugin_name, check_plugins)
            if plugin is None:
                # plug-in can only be None if we looked for the "Unimplemented check..." description.
                # In this case we can run into the 'not found' case below.
                continue

            yield _FoundService(
                service_info={
                    "origin": "auto",
                    "checktype": str(plugin.name),
                    "checkgroup": str(plugin.check_ruleset_name),
                    "item": service.item,
                    "inv_parameters": service.discovered_parameters,
                    "factory_settings": plugin.check_default_parameters,
                    # effective parameters:
                    "parameters": service.parameters.preview(timeperiod_active),
                },
                discovered_labels=service.discovered_labels,
            )
            return

    @staticmethod
    def _search_classical_checks(
        config_cache: ConfigCache,
        host_name: HostName,
        servicedesc: str,
    ) -> Iterable[_FoundService]:
        for entry in config_cache.custom_checks(host_name):
            desc = entry["service_description"]
            if desc == servicedesc:
                result: ServiceInfo = {
                    "origin": "classic",
                }
                if "command_line" in entry:  # Only active checks have a command line
                    result["command_line"] = entry["command_line"]
                yield _FoundService(service_info=result, discovered_labels={})
                return

    @staticmethod
    def _search_active_checks(
        config_cache: ConfigCache,
        host_name: HostName,
        ip_address_of: config.IPLookup,
        servicedesc: str,
    ) -> Iterable[_FoundService]:
        password_store_file = cmk.utils.password_store.pending_password_store_path()

        for active_service in config_cache.active_check_services(
            host_name,
            config_cache.get_host_attributes(host_name, ip_address_of),
            ip_address_of,
            cmk.utils.password_store.load(password_store_file),
            password_store_file,
        ):
            if active_service.description == servicedesc:
                yield _FoundService(
                    service_info={
                        "origin": "active",
                        "checktype": active_service.plugin_name,
                        "parameters": active_service.configuration,
                    },
                    discovered_labels={},
                )
                return


automations.register(AutomationAnalyseServices())


class AutomationAnalyseHost(Automation):
    cmd = "analyse-host"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> AnalyseHostResult:
        host_name = HostName(args[0])

        if loading_result is None:
            loading_result = load_config(discovery_rulesets=())
        loading_result.config_cache.ruleset_matcher.ruleset_optimizer.set_all_processed_hosts(
            {host_name}
        )
        return AnalyseHostResult(
            loading_result.config_cache.labels(host_name),
            loading_result.config_cache.label_sources(host_name),
        )


automations.register(AutomationAnalyseHost())


class AutomationAnalyzeHostRuleMatches(Automation):
    cmd = "analyze-host-rule-matches"
    needs_config = True
    needs_checks = False

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> AnalyzeHostRuleMatchesResult:
        host_name = HostName(args[0])
        # We read the list of rules from stdin since it could be too much for the command line
        match_rules = ast.literal_eval(sys.stdin.read())

        if loading_result is None:
            loading_result = load_config(discovery_rulesets=())
        ruleset_matcher = loading_result.config_cache.ruleset_matcher
        ruleset_matcher.ruleset_optimizer.set_all_processed_hosts({host_name})

        return AnalyzeHostRuleMatchesResult(
            {
                rules[0]["id"]: list(ruleset_matcher.get_host_values(host_name, rules))
                # The caller needs to get one result per rule. For this reason we can not just use
                # the list of rules with the ruleset matching functions but have to execute rule
                # matching for the rules individually. If we would use the provided list of rules,
                # then the not matching rules would not be represented in the result and we would
                # not know which matched value is related to which rule.
                for rules in match_rules
            }
        )


automations.register(AutomationAnalyzeHostRuleMatches())


class AutomationAnalyzeServiceRuleMatches(Automation):
    cmd = "analyze-service-rule-matches"
    needs_config = True
    needs_checks = False

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> AnalyzeServiceRuleMatchesResult:
        host_name = HostName(args[0])
        # This is not necessarily a service description. Can also be an item name when matching
        # checkgroup rules.
        service_or_item = args[1]

        # We read the list of rules from stdin since it could be too much for the command line
        match_rules, service_labels = ast.literal_eval(sys.stdin.read())

        if loading_result is None:
            loading_result = load_config(discovery_rulesets=())
        ruleset_matcher = loading_result.config_cache.ruleset_matcher
        ruleset_matcher.ruleset_optimizer.set_all_processed_hosts({host_name})

        return AnalyzeServiceRuleMatchesResult(
            {
                rules[0]["id"]: list(
                    ruleset_matcher._get_service_ruleset_values(
                        host_name,
                        service_or_item,
                        service_labels,
                        rules,
                    )
                )
                # The caller needs to get one result per rule. For this reason we can not just
                # use the list of rules with the ruleset matching functions but have to execute
                # rule matching for the rules individually. If we would use the provided list of
                # rules, then the not matching rules would not be represented in the result and
                # we would not know which matched value is related to which rule.
                for rules in match_rules
            }
        )


automations.register(AutomationAnalyzeServiceRuleMatches())


class ABCDeleteHosts:
    def _execute(self, args: list[str]) -> None:
        for hostname_str in args:
            self._delete_host_files(HostName(hostname_str))

    @abc.abstractmethod
    def _single_file_paths(self, hostname: HostName) -> Iterable[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _delete_host_files(self, hostname: HostName) -> None:
        raise NotImplementedError()

    def _delete_datasource_dirs(self, hostname: HostName) -> None:
        try:
            ds_directories = os.listdir(data_source_cache_dir)
        except FileNotFoundError:
            ds_directories = []

        for data_source_name in ds_directories:
            filename = f"{data_source_cache_dir}/{data_source_name}/{hostname}"
            self._delete_if_exists(filename)

    def _delete_baked_agents(self, hostname: HostName) -> None:
        # softlinks for baked agents. obsolete packages are removed upon next bake action
        # TODO: Move to bakery code
        baked_agents_dir = var_dir + "/agents/"
        if os.path.exists(baked_agents_dir):
            for folder in os.listdir(baked_agents_dir):
                self._delete_if_exists(f"{folder}/{hostname}")

    def _delete_logwatch(self, hostname: HostName) -> None:
        with suppress(FileNotFoundError):
            shutil.rmtree(f"{logwatch_dir}/{hostname}")

    def _delete_if_exists(self, path: str) -> None:
        """Delete the given file or folder in case it exists"""
        try:
            os.unlink(path)
        except IsADirectoryError:
            shutil.rmtree(path)
        except FileNotFoundError:
            pass

    def _delete_robotmk_html_log_dir(self, hostname: HostName) -> None:
        with suppress(FileNotFoundError):
            shutil.rmtree(
                # Keep in sync with cmk.cee.robotmk.html_log_dir
                omd_root / "var" / "robotmk" / "html_logs" / hostname
            )


class AutomationDeleteHosts(ABCDeleteHosts, Automation):
    cmd = "delete-hosts"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> DeleteHostsResult:
        self._execute(args)
        return DeleteHostsResult()

    def _single_file_paths(self, hostname: HostName) -> list[str]:
        return [
            f"{precompiled_hostchecks_dir}/{hostname}",
            f"{precompiled_hostchecks_dir}/{hostname}.py",
            f"{autochecks_dir}/{hostname}.mk",
            f"{counters_dir}/{hostname}",
            f"{discovered_host_labels_dir}/{hostname}.mk",
            f"{tcp_cache_dir}/{hostname}",
            f"{var_dir}/persisted/{hostname}",
            f"{var_dir}/inventory/{hostname}",
            f"{var_dir}/inventory/{hostname}.gz",
            f"{var_dir}/agent_deployment/{hostname}",
        ]

    def _delete_host_files(self, hostname: HostName) -> None:
        """
        The inventory_archive as well as the performance data is kept
        we do not want to loose any historic data for accidentally deleted hosts.

        These files are cleaned up by the disk space mechanism.
        """
        for path in self._single_file_paths(hostname):
            self._delete_if_exists(path)

        self._delete_datasource_dirs(hostname)
        self._delete_baked_agents(hostname)
        self._delete_logwatch(hostname)
        self._delete_robotmk_html_log_dir(hostname)


automations.register(AutomationDeleteHosts())


class AutomationDeleteHostsKnownRemote(ABCDeleteHosts, Automation):
    """Cleanup automation call for hosts that were previously located on the
    local site and are now handled by a remote site"""

    cmd = "delete-hosts-known-remote"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> DeleteHostsKnownRemoteResult:
        self._execute(args)
        return DeleteHostsKnownRemoteResult()

    def _single_file_paths(self, hostname: HostName) -> list[str]:
        return [
            f"{precompiled_hostchecks_dir}/{hostname}",
            f"{precompiled_hostchecks_dir}/{hostname}.py",
            f"{autochecks_dir}/{hostname}.mk",
            f"{counters_dir}/{hostname}",
            f"{tcp_cache_dir}/{hostname}",
            f"{var_dir}/persisted/{hostname}",
        ]

    def _delete_host_files(self, hostname: HostName) -> None:
        """
        The following locations are skipped on local sites for hosts only known
        on remote sites:
        - var/check_mk/agent_deployment
        - var/check_mk/agents
        """
        for path in self._single_file_paths(hostname):
            self._delete_if_exists(path)

        self._delete_datasource_dirs(hostname)
        self._delete_logwatch(hostname)
        self._delete_robotmk_html_log_dir(hostname)


automations.register(AutomationDeleteHostsKnownRemote())


class AutomationRestart(Automation):
    cmd = "restart"

    def _mode(self) -> CoreAction:
        if config.monitoring_core == "cmc" and not self._check_plugins_have_changed():
            return CoreAction.RELOAD
        return CoreAction.RESTART

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> RestartResult:
        if args:
            nodes = {HostName(hn) for hn in args}
        else:
            nodes = None

        if plugins is None:  # TODO: do we need these?
            plugins = load_plugins()
        if loading_result is None:
            loading_result = load_config(
                discovery_rulesets=agent_based_register.extract_known_discovery_rulesets(plugins)
            )

        hosts_config = config.make_hosts_config()
        ip_address_of = config.ConfiguredIPLookup(
            loading_result.config_cache, error_handler=ip_lookup.CollectFailedHosts()
        )
        return _execute_silently(
            loading_result.config_cache,
            self._mode(),
            ip_address_of,
            hosts_config,
            loading_result.loaded_config,
            plugins,
            hosts_to_update=nodes,
        )

    def _check_plugins_have_changed(self) -> bool:
        last_time = self._time_of_last_core_restart()
        for checks_path in [
            local_checks_dir,
            local_agent_based_plugins_dir,
        ]:
            if not checks_path.exists():
                continue
            this_time = self._last_modification_in_dir(checks_path)
            if this_time > last_time:
                return True
        return False

    def _last_modification_in_dir(self, dir_path: Path) -> float:
        max_time = os.stat(dir_path).st_mtime
        for file_name in os.listdir(dir_path):
            max_time = max(max_time, os.stat(str(dir_path) + "/" + file_name).st_mtime)
        return max_time

    def _time_of_last_core_restart(self) -> float:
        if config.monitoring_core == "cmc":
            pidfile_path = omd_root / "tmp/run/cmc.pid"
        else:
            pidfile_path = omd_root / "tmp/lock/nagios.lock"

        try:
            return pidfile_path.stat().st_mtime
        except FileNotFoundError:
            return 0.0


automations.register(AutomationRestart())


class AutomationReload(AutomationRestart):
    cmd = "reload"

    def _mode(self) -> CoreAction:
        if self._check_plugins_have_changed():
            return CoreAction.RESTART
        return CoreAction.RELOAD

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> ReloadResult:
        return ReloadResult(super().execute(args, plugins, loading_result).config_warnings)


automations.register(AutomationReload())


def _execute_silently(
    config_cache: ConfigCache,
    action: CoreAction,
    ip_address_of: config.ConfiguredIPLookup[ip_lookup.CollectFailedHosts],
    hosts_config: Hosts,
    loaded_config: config.LoadedConfigFragment,
    plugins: AgentBasedPlugins,
    hosts_to_update: set[HostName] | None = None,
    skip_config_locking_for_bakery: bool = False,
) -> RestartResult:
    with redirect_stdout(open(os.devnull, "w")):
        # The IP lookup used to write to stdout, that is not the case anymore.
        # The redirect might not be needed anymore.
        log.setup_console_logging()
        try:
            do_restart(
                config_cache,
                ip_address_of,
                create_core(config.monitoring_core),
                plugins,
                action=action,
                all_hosts=hosts_config.hosts,
                discovery_rules=loaded_config.discovery_rules,
                hosts_to_update=hosts_to_update,
                locking_mode=config.restart_locking,
                duplicates=sorted(
                    hosts_config.duplicates(
                        lambda hn: config_cache.is_active(hn) and config_cache.is_online(hn)
                    )
                ),
                skip_config_locking_for_bakery=skip_config_locking_for_bakery,
            )
        except (MKBailOut, MKGeneralException) as e:
            raise MKAutomationError(str(e))

        except Exception as e:
            if cmk.ccc.debug.enabled():
                raise
            raise MKAutomationError(str(e))

        return RestartResult(
            config_warnings.get_configuration(
                additional_warnings=ip_address_of.error_handler.format_errors()
            )
        )


class AutomationGetConfiguration(Automation):
    # Automation call to get the default configuration
    cmd = "get-configuration"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> GetConfigurationResult:
        called_from_automation_helper = plugins is not None or loading_result is not None
        if called_from_automation_helper:
            raise RuntimeError(
                "This automation call should never be called from the automation helper "
                "as it can only return the active config and we want the default config."
            )

        # We read the list of variable names from stdin since
        # that could be too much for the command line
        variable_names = ast.literal_eval(sys.stdin.read())

        config.load(discovery_rulesets=(), with_conf_d=False)

        result = {}
        for varname in variable_names:
            if hasattr(config, varname):
                value = getattr(config, varname)
                if not hasattr(value, "__call__"):
                    result[varname] = value
        return GetConfigurationResult(result)


automations.register(AutomationGetConfiguration())


class AutomationGetCheckInformation(Automation):
    cmd = "get-check-information"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> GetCheckInformationResult:
        man_page_path_map = man_pages.make_man_page_path_map(
            discover_families(raise_errors=cmk.ccc.debug.enabled()), PluginGroup.CHECKMAN.value
        )
        plugins = plugins or load_plugins()

        plugin_infos: dict[str, dict[str, Any]] = {}
        for plugin in plugins.check_plugins.values():
            plugin_info = plugin_infos.setdefault(
                str(plugin.name),
                {
                    "title": self._get_title(man_page_path_map, plugin.name),
                    "name": str(plugin.name),
                    "service_description": str(plugin.service_name),
                },
            )
            if plugin.check_ruleset_name:
                plugin_info["check_ruleset_name"] = str(plugin.check_ruleset_name)
                plugin_info["check_default_parameters"] = plugin.check_default_parameters
                # TODO: kept for compatibility. See if we can drop this.
                plugin_info["group"] = str(plugin.check_ruleset_name)
            if plugin.discovery_ruleset_name:
                plugin_info["discovery_ruleset_name"] = str(plugin.discovery_ruleset_name)

        return GetCheckInformationResult(plugin_infos)

    @staticmethod
    def _get_title(man_page_path_map: Mapping[str, Path], plugin_name: CheckPluginName) -> str:
        try:
            manfile = man_page_path_map[str(plugin_name)]
        except KeyError:
            return str(plugin_name)

        try:
            return cmk.utils.man_pages.get_title_from_man_page(manfile)
        except Exception as e:
            if cmk.ccc.debug.enabled():
                raise
            raise MKAutomationError(f"Failed to parse man page '{plugin_name}': {e}")


automations.register(AutomationGetCheckInformation())


class AutomationGetSectionInformation(Automation):
    cmd = "get-section-information"

    def execute(
        self,
        args: object,
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> GetSectionInformationResult:
        plugins = plugins or load_plugins()
        section_infos = {
            str(section_name): {
                # for now, we need only these two.
                "name": str(section_name),
                "type": "agent",
            }
            for section_name in plugins.agent_sections
        }
        section_infos.update(
            {
                str(section_name): {
                    "name": str(section_name),
                    "type": "snmp",
                }
                for section_name in plugins.snmp_sections
            }
        )
        return GetSectionInformationResult(section_infos)


automations.register(AutomationGetSectionInformation())


class AutomationScanParents(Automation):
    cmd = "scan-parents"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> ScanParentsResult:
        settings = {
            "timeout": int(args[0]),
            "probes": int(args[1]),
            "max_ttl": int(args[2]),
            "ping_probes": int(args[3]),
        }
        hostnames = [HostName(hn) for hn in islice(args, 4, None)]
        if not cmk.base.parent_scan.traceroute_available():
            raise MKAutomationError("Cannot find binary <tt>traceroute</tt> in search path.")

        plugins = plugins or load_plugins()  # do we really still need this?
        loading_result = loading_result or load_config(
            agent_based_register.extract_known_discovery_rulesets(plugins)
        )

        hosts_config = config.make_hosts_config()
        monitoring_host = (
            HostName(config.monitoring_host) if config.monitoring_host is not None else None
        )

        def make_scan_config() -> Mapping[HostName, ScanConfig]:
            return {
                host: loading_result.config_cache.make_parent_scan_config(host)
                for host in itertools.chain(
                    hostnames,
                    hosts_config.hosts,
                    ([HostName(config.monitoring_host)] if config.monitoring_host else ()),
                )
            }

        try:
            gateway_results = cmk.base.parent_scan.scan_parents_of(
                make_scan_config(),
                hosts_config,
                monitoring_host,
                hostnames,
                silent=True,
                settings=settings,
                lookup_ip_address=functools.partial(
                    config.lookup_ip_address, loading_result.config_cache
                ),
            )
            return ScanParentsResult(gateway_results)
        except Exception as e:
            raise MKAutomationError("%s" % e)


automations.register(AutomationScanParents())


def ip_address_of_host(_host_address: HostAddress, _address_family: socket.AddressFamily) -> None:
    # TODO: this adds the restriction of only being able to use NO_IP hosts for now. When having an
    #  implementation for IP hosts, without using the config_cache, this restriction can be removed.
    return None


def get_special_agent_commandline(
    host_config: DiagSpecialAgentHostConfig,
    agent_name: str,
    params: Mapping[str, object],
    password_store_file: Path,
    passwords: Mapping[str, str],
    http_proxies: Mapping[str, Mapping[str, str]],
) -> Iterator[SpecialAgentCommandLine]:
    special_agent = SpecialAgent(
        load_special_agents(raise_errors=cmk.ccc.debug.enabled()),
        host_config.host_name,
        host_config.ip_address,
        config.get_ssc_host_config(
            host_config.host_name,
            host_config.host_alias,
            host_config.host_primary_family,
            host_config.ip_stack_config,
            host_config.host_additional_addresses_ipv4,
            host_config.host_additional_addresses_ipv6,
            host_config.macros,
            ip_address_of_host,
        ),
        host_config.host_attrs,
        http_proxies,
        passwords,
        password_store_file,
        ExecutableFinder(
            cmk.utils.paths.local_special_agents_dir, cmk.utils.paths.special_agents_dir
        ),
    )

    if not params:
        raise MKAutomationError("No special agent parameters provided.")

    yield from special_agent.iter_special_agent_commands(agent_name, params)


class AutomationDiagSpecialAgent(Automation):
    cmd = "diag-special-agent"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> DiagSpecialAgentResult:
        diag_special_agent_input = DiagSpecialAgentInput.deserialize(sys.stdin.read())
        return DiagSpecialAgentResult(
            tuple(
                SpecialAgentResult(*result)
                for result in self._execute_diag_special_agent(diag_special_agent_input)
            )
        )

    @staticmethod
    def _execute_diag_special_agent(
        diag_special_agent_input: DiagSpecialAgentInput,
    ) -> Iterator[tuple[int, str]]:
        # All passwords are provided by the automation call since we cannot rely that the password
        # store is available on the remote site.
        password_store_file = Path(cmk.utils.paths.tmp_dir, f"passwords_temp_{uuid.uuid4()}")
        try:
            cmk.utils.password_store.save(diag_special_agent_input.passwords, password_store_file)
            cmds = get_special_agent_commandline(
                diag_special_agent_input.host_config,
                diag_special_agent_input.agent_name,
                diag_special_agent_input.params,
                password_store_file,
                diag_special_agent_input.passwords,
                diag_special_agent_input.http_proxies,
            )
            for cmd in cmds:
                fetcher = ProgramFetcher(
                    cmdline=cmd.cmdline,
                    stdin=cmd.stdin,
                    is_cmc=diag_special_agent_input.is_cmc,
                )
                with fetcher:
                    fetched = fetcher.fetch(Mode.DISCOVERY)

                if fetched.is_ok():
                    yield (
                        0,
                        ensure_str_with_fallback(
                            fetched.ok,
                            encoding="utf-8",
                            fallback="latin-1",
                        ),
                    )
                else:
                    yield 1, str(fetched.error)
        except Exception as e:
            if cmk.ccc.debug.enabled():
                raise
            yield 1, str(e)
        finally:
            if password_store_file.exists():
                password_store_file.unlink()


automations.register(AutomationDiagSpecialAgent())


class AutomationDiagHost(Automation):
    cmd = "diag-host"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> DiagHostResult:
        host_name = HostName(args[0])
        test, ipaddress, snmp_community = args[1:4]
        ipaddress = HostAddress(ipaddress)
        agent_port, snmp_timeout, snmp_retries = map(int, args[4:7])

        plugins = plugins or load_plugins()
        loading_result = loading_result or load_config(
            agent_based_register.extract_known_discovery_rulesets(plugins)
        )
        loading_result.config_cache.ruleset_matcher.ruleset_optimizer.set_all_processed_hosts(
            {host_name}
        )

        # In 1.5 the tcp connect timeout has been added. The automation may
        # be called from a remote site with an older version. For this reason
        # we need to deal with the old args.
        if len(args) == 14:
            tcp_connect_timeout = None
            cmd = args[7]
        else:
            tcp_connect_timeout = float(args[7])
            cmd = args[8]

        snmpv3_use = None
        snmpv3_auth_proto = None
        snmpv3_security_name = None
        snmpv3_security_password = None
        snmpv3_privacy_proto = None
        snmpv3_privacy_password = None

        if len(args) > 9:
            snmpv3_use = args[9]
            if snmpv3_use in ["authNoPriv", "authPriv"]:
                snmpv3_auth_proto, snmpv3_security_name, snmpv3_security_password = args[10:13]
            else:
                snmpv3_security_name = args[11]
            if snmpv3_use == "authPriv":
                snmpv3_privacy_proto, snmpv3_privacy_password = args[13:15]

        # No caching option over commandline here.
        file_cache_options = FileCacheOptions()

        if not ipaddress:
            if ConfigCache.ip_stack_config(host_name) is ip_lookup.IPStackConfig.NO_IP:
                raise MKGeneralException("Host is configured as No-IP host: %s" % host_name)
            try:
                resolved_address = config.lookup_ip_address(loading_result.config_cache, host_name)
            except Exception:
                raise MKGeneralException("Cannot resolve host name %s into IP address" % host_name)

            if resolved_address is None:
                raise MKGeneralException("Cannot resolve host name %s into IP address" % host_name)

            ipaddress = resolved_address

        try:
            if test == "ping":
                return DiagHostResult(
                    *self._execute_ping(loading_result.config_cache, host_name, ipaddress)
                )

            if test == "agent":
                return DiagHostResult(
                    *self._execute_agent(
                        loading_result.config_cache,
                        loading_result.config_cache.make_service_configurer(plugins.check_plugins),
                        plugins,
                        host_name,
                        ipaddress,
                        agent_port=agent_port,
                        cmd=cmd,
                        tcp_connect_timeout=tcp_connect_timeout,
                        file_cache_options=file_cache_options,
                        # Passing `ip_address_of` is the result of a refactoring.
                        # We do pass an IP address as well, so I'm not quite sure why we need this.
                        # Feel free to investigate!
                        # Also: This class might write to console. The de-serializer of the automation call will
                        # not be able to handle this I think? At best it will ignore it. We should fix this.
                        ip_address_of=config.ConfiguredIPLookup(
                            loading_result.config_cache,
                            error_handler=config.handle_ip_lookup_failure,
                        ),
                    )
                )

            if test == "traceroute":
                return DiagHostResult(
                    *self._execute_traceroute(loading_result.config_cache, host_name, ipaddress)
                )

            if test.startswith("snmp"):
                if config.simulation_mode:
                    raise MKSNMPError(
                        "Simulation mode enabled. Not trying to contact snmp datasource"
                    )
                return DiagHostResult(
                    *self._execute_snmp(
                        loading_result.config_cache,
                        test,
                        loading_result.config_cache.make_snmp_config(
                            host_name, ipaddress, SourceType.HOST, backend_override=None
                        ),
                        host_name,
                        ipaddress,
                        snmp_community,
                        snmp_timeout,
                        snmp_retries,
                        snmpv3_use,
                        snmpv3_auth_proto,
                        snmpv3_security_name,
                        snmpv3_security_password,
                        snmpv3_privacy_proto,
                        snmpv3_privacy_password,
                    )
                )

            return DiagHostResult(
                1,
                "Command not implemented",
            )

        except Exception as e:
            if cmk.ccc.debug.enabled():
                raise
            return DiagHostResult(
                1,
                str(e),
            )

    def _execute_ping(
        self, config_cache: ConfigCache, hostname: HostName, ipaddress: str
    ) -> tuple[int, str]:
        base_cmd = (
            "ping6" if config_cache.default_address_family(hostname) is socket.AF_INET6 else "ping"
        )
        completed_process = subprocess.run(
            [base_cmd, "-A", "-i", "0.2", "-c", "2", "-W", "5", ipaddress],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
            check=False,
        )
        return completed_process.returncode, completed_process.stdout

    def _execute_agent(
        self,
        config_cache: ConfigCache,
        service_configurer: ServiceConfigurer,
        plugins: AgentBasedPlugins,
        host_name: HostName,
        ipaddress: HostAddress,
        *,
        agent_port: int,
        cmd: str,
        tcp_connect_timeout: float | None,
        file_cache_options: FileCacheOptions,
        ip_address_of: config.IPLookup,
    ) -> tuple[int, str]:
        hosts_config = config_cache.hosts_config
        check_interval = config_cache.check_mk_check_interval(host_name)
        oid_cache_dir = Path(cmk.utils.paths.snmp_scan_cache_dir)
        stored_walk_path = Path(cmk.utils.paths.snmpwalks_dir)
        walk_cache_path = Path(cmk.utils.paths.var_dir) / "snmp_cache"
        file_cache_path = Path(cmk.utils.paths.data_source_cache_dir)
        tcp_cache_path = Path(cmk.utils.paths.tcp_cache_dir)
        tls_config = TLSConfig(
            cas_dir=Path(cmk.utils.paths.agent_cas_dir),
            ca_store=Path(cmk.utils.paths.agent_cert_store),
            site_crt=Path(cmk.utils.paths.site_cert_file),
        )

        state, output = 0, ""
        pending_passwords_file = cmk.utils.password_store.pending_password_store_path()
        passwords = cmk.utils.password_store.load(pending_passwords_file)
        snmp_scan_config = SNMPScanConfig(
            on_error=OnError.RAISE,
            missing_sys_description=config_cache.missing_sys_description(host_name),
            oid_cache_dir=oid_cache_dir,
        )
        for source in sources.make_sources(
            plugins,
            host_name,
            ipaddress,
            ConfigCache.ip_stack_config(host_name),
            fetcher_factory=config_cache.fetcher_factory(service_configurer),
            snmp_fetcher_config=SNMPFetcherConfig(
                scan_config=snmp_scan_config,
                selected_sections=NO_SELECTION,
                backend_override=None,
                stored_walk_path=stored_walk_path,
                walk_cache_path=walk_cache_path,
            ),
            is_cluster=host_name in hosts_config.clusters,
            simulation_mode=config.simulation_mode,
            file_cache_options=file_cache_options,
            file_cache_max_age=MaxAge(
                checking=config.check_max_cachefile_age,
                discovery=1.5 * check_interval,
                inventory=1.5 * check_interval,
            ),
            snmp_backend=config_cache.get_snmp_backend(host_name),
            file_cache_path=file_cache_path,
            tcp_cache_path=tcp_cache_path,
            tls_config=tls_config,
            computed_datasources=config_cache.computed_datasources(host_name),
            datasource_programs=config_cache.datasource_programs(host_name),
            tag_list=config_cache.tag_list(host_name),
            management_ip=lookup_mgmt_board_ip_address(config_cache, host_name),
            management_protocol=config_cache.management_protocol(host_name),
            special_agent_command_lines=config_cache.special_agent_command_lines(
                host_name,
                ipaddress,
                password_store_file=pending_passwords_file,
                passwords=passwords,
                ip_address_of=ConfiguredIPLookup(
                    config_cache, error_handler=handle_ip_lookup_failure
                ),
            ),
            agent_connection_mode=config_cache.agent_connection_mode(host_name),
            check_mk_check_interval=config_cache.check_mk_check_interval(host_name),
        ):
            source_info = source.source_info()
            if source_info.fetcher_type is FetcherType.SNMP:
                continue

            fetcher = source.fetcher()
            if source_info.fetcher_type is FetcherType.PROGRAM and cmd:
                assert isinstance(fetcher, ProgramFetcher)
                fetcher = ProgramFetcher(
                    cmdline=config_cache.translate_commandline(
                        host_name, ipaddress, cmd, ip_address_of
                    ),
                    stdin=fetcher.stdin,
                    is_cmc=fetcher.is_cmc,
                )
            elif source_info.fetcher_type is FetcherType.TCP:
                assert isinstance(fetcher, TCPFetcher)
                port = agent_port or fetcher.address[1]
                timeout = tcp_connect_timeout or fetcher.timeout
                fetcher = TCPFetcher(
                    family=fetcher.family,
                    address=(fetcher.address[0], port),
                    timeout=timeout,
                    host_name=fetcher.host_name,
                    encryption_handling=fetcher.encryption_handling,
                    pre_shared_secret=fetcher.pre_shared_secret,
                    tls_config=tls_config,
                )

            raw_data = get_raw_data(
                source.file_cache(
                    simulation=config.simulation_mode,
                    file_cache_options=file_cache_options,
                ),
                fetcher,
                Mode.CHECKING,
            )
            if raw_data.is_ok():
                # We really receive a byte string here. The agent sections
                # may have different encodings and are normally decoded one
                # by one (AgentChecker._parse_host_section).  For the
                # moment we use UTF-8 with fallback to latin-1 by default,
                # similar to the AgentChecker, but we do not
                # respect the ecoding options of sections.
                # If this is a problem, we would have to apply parse and
                # decode logic and unparse the decoded output again.
                output += ensure_str_with_fallback(
                    raw_data.ok,
                    encoding="utf-8",
                    fallback="latin-1",
                )
            else:
                state = 1
                output += str(raw_data.error)

        return state, output

    def _execute_traceroute(
        self, config_cache: ConfigCache, hostname: HostName, ipaddress: str
    ) -> tuple[int, str]:
        family_flag = (
            "-6" if config_cache.default_address_family(hostname) is socket.AF_INET6 else "-4"
        )
        try:
            completed_process = subprocess.run(
                ["traceroute", family_flag, "-n", ipaddress],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                encoding="utf-8",
                check=False,
            )
        except FileNotFoundError:
            return 1, "Cannot find binary <tt>traceroute</tt>."
        return completed_process.returncode, completed_process.stdout

    def _execute_snmp(
        self,
        config_cache: ConfigCache,
        test: str,
        snmp_config: SNMPHostConfig,
        hostname: HostName,
        ipaddress: HostAddress,
        snmp_community: str,
        snmp_timeout: int,
        snmp_retries: int,
        snmpv3_use: str | None,
        snmpv3_auth_proto: str | None,
        snmpv3_security_name: str | None,
        snmpv3_security_password: str | None,
        snmpv3_privacy_proto: str | None,
        snmpv3_privacy_password: str | None,
    ) -> tuple[int, str]:
        # SNMPv3 tuples
        # ('noAuthNoPriv', "username")
        # ('authNoPriv', 'md5', '11111111', '22222222')
        # ('authPriv', 'md5', '11111111', '22222222', 'DES', '33333333')

        if test == "snmpv3":
            credentials: SNMPCredentials = snmp_config.credentials

            if snmpv3_use:
                snmpv3_credentials = [snmpv3_use]
                if snmpv3_use in ["authNoPriv", "authPriv"]:
                    if (
                        not isinstance(snmpv3_auth_proto, str)
                        or not isinstance(snmpv3_security_name, str)
                        or not isinstance(snmpv3_security_password, str)
                    ):
                        raise TypeError()
                    snmpv3_credentials.extend(
                        [snmpv3_auth_proto, snmpv3_security_name, snmpv3_security_password]
                    )
                else:
                    if not isinstance(snmpv3_security_name, str):
                        raise TypeError()
                    snmpv3_credentials.extend([snmpv3_security_name])

                if snmpv3_use == "authPriv":
                    if not isinstance(snmpv3_privacy_proto, str) or not isinstance(
                        snmpv3_privacy_password, str
                    ):
                        raise TypeError()
                    snmpv3_credentials.extend([snmpv3_privacy_proto, snmpv3_privacy_password])

                credentials = tuple(snmpv3_credentials)
        else:
            credentials = snmp_community or (
                snmp_config.credentials
                if isinstance(snmp_config.credentials, str)
                else snmp_default_community
            )

        # Determine SNMPv2/v3 community
        if hostname not in config.explicit_snmp_communities:
            cred = config_cache.snmp_credentials_of_version(
                hostname, snmp_version=3 if test == "snmpv3" else 2
            )
            if cred is not None:
                credentials = cred

        # SNMP versions
        match test:
            case "snmpv1":
                snmp_version = SNMPVersion.V1
                bulkwalk_enabled = False  # not implemented in v1 anyway
            case "snmpv2":
                snmp_version = SNMPVersion.V2C
                bulkwalk_enabled = True
            case "snmpv2_nobulk":
                snmp_version = SNMPVersion.V2C
                bulkwalk_enabled = False
            case "snmpv3":
                snmp_version = SNMPVersion.V3
                bulkwalk_enabled = True
            case other:
                return 1, f"SNMP command {other!r} not implemented"

        # TODO: What about SNMP management boards?
        # TODO: `get_snmp_table()` with some cache handling
        #       is what the SNMPFetcher already does.  Work on reducing
        #       code duplication.
        snmp_config = SNMPHostConfig(
            is_ipv6_primary=snmp_config.is_ipv6_primary,
            hostname=hostname,
            ipaddress=ipaddress,
            credentials=credentials,
            port=snmp_config.port,
            snmp_version=snmp_version,
            bulkwalk_enabled=bulkwalk_enabled,
            bulk_walk_size_of=snmp_config.bulk_walk_size_of,
            timing={
                "timeout": snmp_timeout,
                "retries": snmp_retries,
            },
            oid_range_limits=snmp_config.oid_range_limits,
            snmpv3_contexts=snmp_config.snmpv3_contexts,
            character_encoding=snmp_config.character_encoding,
            snmp_backend=snmp_config.snmp_backend,
        )

        stored_walk_path = Path(cmk.utils.paths.snmpwalks_dir)
        data = get_snmp_table(
            section_name=None,
            tree=BackendSNMPTree(
                base=".1.3.6.1.2.1.1",
                oids=[BackendOIDSpec(c, "string", False) for c in "1456"],
            ),
            walk_cache={},
            backend=make_snmp_backend(snmp_config, log.logger, stored_walk_path=stored_walk_path),
            log=log.logger.debug,
        )

        if data:
            return 0, "sysDescr:\t%s\nsysContact:\t%s\nsysName:\t%s\nsysLocation:\t%s\n" % tuple(
                data[0]
            )

        return 1, "Got empty SNMP response"


automations.register(AutomationDiagHost())


class AutomationActiveCheck(Automation):
    cmd = "active-check"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> ActiveCheckResult:
        host_name = HostName(args[0])
        plugin, item = args[1:]

        plugins = plugins or load_plugins()  # do we really still need this?
        loading_result = loading_result or load_config(
            agent_based_register.extract_known_discovery_rulesets(plugins)
        )
        config_cache = loading_result.config_cache
        config_cache.ruleset_matcher.ruleset_optimizer.set_all_processed_hosts({host_name})

        # Maybe we add some meaningfull error handling here someday?
        # This reflects the effetive behavior when the error handler was inroduced.
        ip_address_of = config.ConfiguredIPLookup(config_cache, error_handler=lambda *a, **kw: None)

        if plugin == "custom":
            for entry in config_cache.custom_checks(host_name):
                if entry["service_description"] != item:
                    continue

                command_line = self._replace_macros(
                    host_name,
                    entry["service_description"],
                    entry.get("command_line", ""),
                    ip_address_of,
                    discovered_labels={},
                    config_cache=config_cache,
                )
                if command_line:
                    cmd = core_config.autodetect_plugin(command_line)
                    return ActiveCheckResult(*self._execute_check_plugin(cmd))

                return ActiveCheckResult(
                    -1,
                    "Passive check - cannot be executed",
                )

        with redirect_stdout(open(os.devnull, "w")):
            # The IP lookup used to write to stdout, that is not the case anymore.
            # The redirect might not be needed anymore.
            host_attrs = config_cache.get_host_attributes(host_name, ip_address_of)

        password_store_file = cmk.utils.password_store.pending_password_store_path()
        for service_data in config_cache.active_check_services(
            host_name,
            host_attrs,
            ip_address_of,
            cmk.utils.password_store.load(password_store_file),
            password_store_file,
            single_plugin=plugin,
        ):
            if service_data.description != item:
                continue

            command_line = self._replace_service_macros(
                host_name,
                service_data.description,
                config_cache.ruleset_matcher.labels_of_service(
                    host_name, service_data.description, {}
                ),
                " ".join(service_data.command),
                config_cache=config_cache,
            )
            return ActiveCheckResult(*self._execute_check_plugin(command_line))

        return ActiveCheckResult(
            None,
            "Failed to compute check result",
        )

    # Simulate replacing some of the more important macros of host and service. We
    # cannot use dynamic macros, of course. Note: this will not work
    # without OMD, since we do not know the value of $USER1$ and $USER2$
    # here. We could read the Nagios resource.cfg file, but we do not
    # know for sure the place of that either.
    def _replace_macros(
        self,
        hostname: HostName,
        service_desc: str,
        commandline: str,
        ip_address_of: config.IPLookup,
        discovered_labels: Mapping[str, str],
        config_cache: ConfigCache,
    ) -> str:
        macros = ConfigCache.get_host_macros_from_attributes(
            hostname, config_cache.get_host_attributes(hostname, ip_address_of)
        )

        service_attrs = core_config.get_service_attributes(
            config_cache,
            hostname,
            service_desc,
            config_cache.ruleset_matcher.labels_of_service(
                hostname, service_desc, discovered_labels
            ),
            extra_icon=None,
        )
        macros.update(ConfigCache.get_service_macros_from_attributes(service_attrs))
        macros.update(config.get_resource_macros())

        return replace_macros_in_str(commandline, {k: f"{v}" for k, v in macros.items()})

    def _replace_service_macros(
        self,
        host_name: HostName,
        service_name: ServiceName,
        service_labels: Mapping[str, str],
        commandline: str,
        config_cache: ConfigCache,
    ) -> str:
        service_attrs = core_config.get_service_attributes(
            config_cache, host_name, service_name, service_labels, extra_icon=None
        )
        service_macros = ConfigCache.get_service_macros_from_attributes(service_attrs)

        return replace_macros_in_str(commandline, {k: f"{v}" for k, v in service_macros.items()})

    def _execute_check_plugin(self, commandline: str) -> tuple[ServiceState, ServiceDetails]:
        try:
            result = subprocess.run(
                shlex.split(commandline),
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )

            status = result.returncode if result.returncode in [0, 1, 2] else 3
            output = result.stdout.strip().decode().split("|", 1)[0]  # Drop performance data

            return status, output

        except Exception as e:
            if cmk.ccc.debug.enabled():
                raise
            return 3, "UNKNOWN - Cannot execute command: %s" % e


automations.register(AutomationActiveCheck())


class AutomationUpdatePasswordsMergedFile(Automation):
    cmd = "update-passwords-merged-file"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> UpdatePasswordsMergedFileResult:
        loading_result = loading_result or load_config(discovery_rulesets=())
        cmk.utils.password_store.save(
            loading_result.config_cache.collect_passwords(),
            cmk.utils.password_store.pending_password_store_path(),
        )
        return UpdatePasswordsMergedFileResult()


automations.register(AutomationUpdatePasswordsMergedFile())


class AutomationUpdateDNSCache(Automation):
    cmd = "update-dns-cache"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> UpdateDNSCacheResult:
        plugins = plugins or load_plugins()  # can we remove this?
        loading_result = loading_result or load_config(
            agent_based_register.extract_known_discovery_rulesets(plugins)
        )

        hosts_config = loading_result.config_cache.hosts_config
        return UpdateDNSCacheResult(
            *ip_lookup.update_dns_cache(
                ip_lookup_configs=(
                    loading_result.config_cache.ip_lookup_config(hn)
                    for hn in frozenset(itertools.chain(hosts_config.hosts, hosts_config.clusters))
                    if loading_result.config_cache.is_active(hn)
                    and loading_result.config_cache.is_online(hn)
                ),
                configured_ipv4_addresses=config.ipaddresses,
                configured_ipv6_addresses=config.ipv6addresses,
                simulation_mode=config.simulation_mode,
                override_dns=HostAddress(config.fake_dns) if config.fake_dns is not None else None,
            )
        )


automations.register(AutomationUpdateDNSCache())


class AutomationGetAgentOutput(Automation):
    cmd = "get-agent-output"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> GetAgentOutputResult:
        hostname = HostName(args[0])
        ty = args[1]

        plugins = plugins or load_plugins()  # do we really still need this?
        loading_result = loading_result or load_config(
            agent_based_register.extract_known_discovery_rulesets(plugins)
        )
        service_configurer = loading_result.config_cache.make_service_configurer(
            plugins.check_plugins
        )
        config_cache = loading_result.config_cache
        hosts_config = config.make_hosts_config()

        # No caching option over commandline here.
        file_cache_options = FileCacheOptions()

        success = True
        output = ""
        info = b""

        try:
            ip_stack_config = ConfigCache.ip_stack_config(hostname)
            ipaddress = (
                None
                if ip_stack_config is ip_lookup.IPStackConfig.NO_IP
                else config.lookup_ip_address(config_cache, hostname)
            )
            check_interval = config_cache.check_mk_check_interval(hostname)
            stored_walk_path = Path(cmk.utils.paths.snmpwalks_dir)
            walk_cache_path = Path(cmk.utils.paths.var_dir) / "snmp_cache"
            section_cache_path = Path(var_dir)
            file_cache_path = Path(cmk.utils.paths.data_source_cache_dir)
            tcp_cache_path = Path(cmk.utils.paths.tcp_cache_dir)
            tls_config = TLSConfig(
                cas_dir=Path(cmk.utils.paths.agent_cas_dir),
                ca_store=Path(cmk.utils.paths.agent_cert_store),
                site_crt=Path(cmk.utils.paths.site_cert_file),
            )
            snmp_scan_config = SNMPScanConfig(
                on_error=OnError.RAISE,
                oid_cache_dir=Path(cmk.utils.paths.snmp_scan_cache_dir),
                missing_sys_description=config_cache.missing_sys_description(hostname),
            )

            if ty == "agent":
                core_password_store_file = cmk.utils.password_store.core_password_store_path(
                    LATEST_CONFIG
                )
                for source in sources.make_sources(
                    plugins,
                    hostname,
                    ipaddress,
                    ip_stack_config,
                    fetcher_factory=config_cache.fetcher_factory(service_configurer),
                    snmp_fetcher_config=SNMPFetcherConfig(
                        scan_config=snmp_scan_config,
                        selected_sections=NO_SELECTION,
                        backend_override=None,
                        stored_walk_path=stored_walk_path,
                        walk_cache_path=walk_cache_path,
                    ),
                    is_cluster=hostname in hosts_config.clusters,
                    simulation_mode=config.simulation_mode,
                    file_cache_options=file_cache_options,
                    file_cache_max_age=MaxAge(
                        checking=config.check_max_cachefile_age,
                        discovery=1.5 * check_interval,
                        inventory=1.5 * check_interval,
                    ),
                    snmp_backend=config_cache.get_snmp_backend(hostname),
                    file_cache_path=file_cache_path,
                    tcp_cache_path=tcp_cache_path,
                    tls_config=tls_config,
                    computed_datasources=config_cache.computed_datasources(hostname),
                    datasource_programs=config_cache.datasource_programs(hostname),
                    tag_list=config_cache.tag_list(hostname),
                    management_ip=lookup_mgmt_board_ip_address(config_cache, hostname),
                    management_protocol=config_cache.management_protocol(hostname),
                    special_agent_command_lines=config_cache.special_agent_command_lines(
                        hostname,
                        ipaddress,
                        password_store_file=core_password_store_file,
                        passwords=cmk.utils.password_store.load(core_password_store_file),
                        ip_address_of=ConfiguredIPLookup(
                            config_cache, error_handler=handle_ip_lookup_failure
                        ),
                    ),
                    agent_connection_mode=config_cache.agent_connection_mode(hostname),
                    check_mk_check_interval=config_cache.check_mk_check_interval(hostname),
                ):
                    source_info = source.source_info()
                    if source_info.fetcher_type is FetcherType.SNMP:
                        continue

                    raw_data = get_raw_data(
                        source.file_cache(
                            simulation=config.simulation_mode, file_cache_options=file_cache_options
                        ),
                        source.fetcher(),
                        Mode.CHECKING,
                    )
                    host_sections = parse_raw_data(
                        make_parser(
                            config_cache.parser_factory(),
                            source_info.hostname,
                            source_info.fetcher_type,
                            persisted_section_dir=make_persisted_section_dir(
                                source_info.hostname,
                                fetcher_type=source_info.fetcher_type,
                                ident=source_info.ident,
                                section_cache_path=section_cache_path,
                            ),
                            keep_outdated=file_cache_options.keep_outdated,
                            logger=logging.getLogger("cmk.base.checking"),
                        ),
                        raw_data,
                        selection=NO_SELECTION,
                    )
                    source_results = summarize(
                        hostname,
                        ipaddress,
                        host_sections,
                        config=config_cache.summary_config(hostname, source_info.ident),
                        fetcher_type=source_info.fetcher_type,
                    )
                    if any(r.state != 0 for r in source_results):
                        # Optionally show errors of problematic data sources
                        success = False
                        output += f"[{source_info.ident}] {', '.join(r.summary for r in source_results)}\n"
                    assert raw_data.ok is not None
                    info += raw_data.ok
            else:
                if not ipaddress:
                    raise MKGeneralException("Failed to gather IP address of %s" % hostname)
                snmp_config = config_cache.make_snmp_config(
                    hostname, ipaddress, SourceType.HOST, backend_override=None
                )
                backend = make_snmp_backend(
                    snmp_config, log.logger, use_cache=False, stored_walk_path=stored_walk_path
                )

                lines = []
                for walk_oid in oids_to_walk():
                    try:
                        for oid, value in walk_for_export(backend.walk(walk_oid, context="")):
                            raw_oid_value = f"{oid} {value}\n"
                            lines.append(raw_oid_value.encode())
                    except Exception as e:
                        if cmk.ccc.debug.enabled():
                            raise
                        success = False
                        output += f"OID '{oid}': {e}\n"

                info = b"".join(lines)
        except Exception as e:
            success = False
            output = f"Failed to fetch data from {hostname}: {e}\n"
            if cmk.ccc.debug.enabled():
                raise

        return GetAgentOutputResult(
            success,
            output,
            AgentRawData(info),
        )


automations.register(AutomationGetAgentOutput())


class AutomationNotificationReplay(Automation):
    cmd = "notification-replay"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> NotificationReplayResult:
        def ensure_nagios(msg: str) -> None:
            if config.is_cmc():
                raise RuntimeError(msg)

        plugins = plugins or load_plugins()  # do we really still need this?
        loading_result = loading_result or load_config(discovery_rulesets=())

        nr = args[0]
        notify.notification_replay_backlog(
            lambda hostname, plugin: loading_result.config_cache.notification_plugin_parameters(
                hostname, plugin
            ),
            config.get_http_proxy,
            ensure_nagios,
            int(nr),
            rules=config.notification_rules,
            parameters=config.notification_parameter,
            define_servicegroups=config.define_servicegroups,
            config_contacts=config.contacts,
            fallback_email=config.notification_fallback_email,
            fallback_format=config.notification_fallback_format,
            plugin_timeout=config.notification_plugin_timeout,
            spooling=ConfigCache.notification_spooling(),
            backlog_size=config.notification_backlog,
            logging_level=ConfigCache.notification_logging_level(),
            all_timeperiods=load_timeperiods(),
        )
        return NotificationReplayResult()


automations.register(AutomationNotificationReplay())


class AutomationNotificationAnalyse(Automation):
    cmd = "notification-analyse"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> NotificationAnalyseResult:
        def ensure_nagios(msg: str) -> None:
            if config.is_cmc():
                raise RuntimeError(msg)

        plugins = plugins or load_plugins()  # do we really still need this?
        loading_result = loading_result or load_config(discovery_rulesets=())

        nr = args[0]
        return NotificationAnalyseResult(
            notify.notification_analyse_backlog(
                lambda hostname, plugin: loading_result.config_cache.notification_plugin_parameters(
                    hostname, plugin
                ),
                config.get_http_proxy,
                ensure_nagios,
                int(nr),
                rules=config.notification_rules,
                parameters=config.notification_parameter,
                define_servicegroups=config.define_servicegroups,
                config_contacts=config.contacts,
                fallback_email=config.notification_fallback_email,
                fallback_format=config.notification_fallback_format,
                plugin_timeout=config.notification_plugin_timeout,
                spooling=ConfigCache.notification_spooling(),
                backlog_size=config.notification_backlog,
                logging_level=ConfigCache.notification_logging_level(),
                all_timeperiods=load_timeperiods(),
            )
        )


automations.register(AutomationNotificationAnalyse())


class AutomationNotificationTest(Automation):
    cmd = "notification-test"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> NotificationTestResult:
        def ensure_nagios(msg: str) -> None:
            if config.is_cmc():
                raise RuntimeError(msg)

        context = json.loads(args[0])
        dispatch = args[1]

        plugins = plugins or load_plugins()  # do we really still need this?
        loading_result = loading_result or load_config(discovery_rulesets=())

        return NotificationTestResult(
            notify.notification_test(
                context,
                lambda hostname, plugin: loading_result.config_cache.notification_plugin_parameters(
                    hostname, plugin
                ),
                config.get_http_proxy,
                ensure_nagios,
                rules=config.notification_rules,
                parameters=config.notification_parameter,
                define_servicegroups=config.define_servicegroups,
                config_contacts=config.contacts,
                fallback_email=config.notification_fallback_email,
                fallback_format=config.notification_fallback_format,
                plugin_timeout=config.notification_plugin_timeout,
                spooling=ConfigCache.notification_spooling(),
                backlog_size=config.notification_backlog,
                logging_level=ConfigCache.notification_logging_level(),
                all_timeperiods=load_timeperiods(),
                dispatch=dispatch,
            )
        )


automations.register(AutomationNotificationTest())


class AutomationGetBulks(Automation):
    cmd = "notification-get-bulks"

    def execute(
        self,
        args: list[str],
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> NotificationGetBulksResult:
        only_ripe = args[0] == "1"
        return NotificationGetBulksResult(
            notify.find_bulks(only_ripe, bulk_interval=config.notification_bulk_interval)
        )


automations.register(AutomationGetBulks())


class AutomationCreateDiagnosticsDump(Automation):
    cmd = "create-diagnostics-dump"

    def execute(
        self,
        args: DiagnosticsCLParameters,
        plugins: AgentBasedPlugins | None,
        loading_result: config.LoadingResult | None,
    ) -> CreateDiagnosticsDumpResult:
        if loading_result is None:
            loading_result = load_config(discovery_rulesets=())
        buf = io.StringIO()
        with redirect_stdout(buf), redirect_stderr(buf):
            log.setup_console_logging()
            # NOTE: All the stuff is logged on this level only, which is below the default WARNING level.
            log.logger.setLevel(logging.INFO)
            dump = DiagnosticsDump(loading_result.loaded_config, deserialize_cl_parameters(args))
            dump.create()
            return CreateDiagnosticsDumpResult(
                output=buf.getvalue(),
                tarfile_path=str(dump.tarfile_path),
                tarfile_created=dump.tarfile_created,
            )


automations.register(AutomationCreateDiagnosticsDump())
