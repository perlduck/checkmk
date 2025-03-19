#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from collections.abc import Mapping, Sequence
from typing import Any

from cmk.base.check_api import get_http_proxy, passwordstore_get_cmdline
from cmk.base.config import special_agent_info


def agent_azure_arguments(  # pylint: disable=too-many-branches
    params: Mapping[str, Any],
    hostname: str,
    ipaddress: str | None,
) -> Sequence[Any]:
    args = [
        "--tenant",
        params["tenant"],
        "--client",
        params["client"],
        "--secret",
        passwordstore_get_cmdline("%s", params["secret"]),
    ]

    keys = ("authority", "subscription", "piggyback_vms")

    for key in (k for k in keys if k in params):
        option = "--%s" % key
        value = params[key]
        if isinstance(value, bool):
            if value:
                args.append(option)
        else:
            args += [option, value]

    if proxy_settings := params.get("proxy"):
        args += ["--proxy", get_http_proxy(proxy_settings).serialize()]

    if "services" in params:
        args += ["--services", *params["services"]]

    config = params["config"]

    explicit = config.get("explicit", [])
    if explicit:
        args.append("--explicit-config")
    for group_dict in explicit:
        group_name = group_dict["group_name"]
        args.append("group=%s" % group_name)

        group_resources = group_dict.get("resources")
        if group_resources:
            args.append("resources=%s" % ",".join(group_resources))

    tag_based = config.get("tag_based", [])
    for tag, requirement in tag_based:
        if requirement == "exists":
            args += ["--require-tag", tag]
        elif isinstance(requirement, tuple) and requirement[0] == "value":
            args += ["--require-tag-value", tag, requirement[1]]

    if (filter_tags := params.get("filter_tags")) is not None:
        match filter_tags[1]:
            case str(tag_key_pattern):
                args += ["--import-matching-tags-as-labels", tag_key_pattern]
            case None:
                args += ["--ignore-all-tags"]

    args += [
        "--cache-id",
        hostname,
    ]
    return args


special_agent_info["azure"] = agent_azure_arguments
