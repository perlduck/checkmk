#!/usr/bin/env python3
# Copyright (C) 2019 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.


from collections.abc import Iterator, Mapping
from typing import Any

from cmk.base.check_api import LegacyCheckDefinition
from cmk.base.check_legacy_includes.temperature import check_temperature
from cmk.base.config import check_info
from cmk.base.plugins.agent_based.utils.temperature import TempParamType as TempParamType

# comNET GmbH, Fabian Binder - 2018-05-30

# .1.3.6.1.4.1.9.9.719.1.41.2.1.2  cpu Unit Name
# .1.3.6.1.4.1.9.9.719.1.41.2.1.10 cucsProcessorEnvStatsTemperature


def inventory_cisco_ucs_temp_cpu(section: Mapping[str, int]) -> Iterator[Any]:
    yield from ((name, {}) for name in section)


def check_cisco_ucs_temp_cpu(
    item: str, params: TempParamType, section: Mapping[str, int]
) -> tuple | None:
    if (temperature := section.get(item)) is None:
        return None

    return check_temperature(temperature, params, f"cisco_temp_{item}")


check_info["cisco_ucs_temp_cpu"] = LegacyCheckDefinition(
    service_name="Temperature CPU %s",
    discovery_function=inventory_cisco_ucs_temp_cpu,
    check_function=check_cisco_ucs_temp_cpu,
    check_ruleset_name="temperature",
    check_default_parameters={
        "levels": (75.0, 85.0),
    },
)
