#!/usr/bin/env python3
# Copyright (C) 2025 Checkmk GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

import pytest

from cmk.gui.wato.pages.notifications.quick_setup import validate_throttling_values

from cmk.rulesets.v1.form_specs.validators import ValidationError


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param((1, 2), id="second value is greater than first"),
        pytest.param((2, 1), id="second value is less than first"),
    ],
)
def test_validate_throttling_values(payload: tuple[int, ...]) -> None:
    assert validate_throttling_values(payload) is None  # type: ignore[func-returns-value]


@pytest.mark.parametrize(
    "payload",
    [
        pytest.param(tuple(), id="no arguments provided"),
        pytest.param((0, 2), id="first value shouldn't be less than 1"),
        pytest.param((1, 0), id="second value shouldn't be less than 1"),
        pytest.param(("foo", 2), id="first value is the wrong type"),
        pytest.param((1, "bar"), id="second value is wrong type"),
        pytest.param((1, 2, 3), id="we only expect two inputs"),
    ],
)
def test_validate_throttling_values_raises(payload: tuple[int, ...]) -> None:
    with pytest.raises(ValidationError):
        validate_throttling_values(payload)
