#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

from cmk.gui import mkeventd
from cmk.gui.mkeventd import send_event

from _pytest.monkeypatch import MonkeyPatch


def test_send_event(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        mkeventd.time,
        "time",
        lambda: 1622638021,
    )
    monkeypatch.setattr(
        mkeventd,
        "execute_command",
        lambda *args, **kwargs: None,
    )
    assert send_event({
        "facility": 17,
        "priority": 1,
        "sl": 20,
        "host": "horst",
        "ipaddress": "127.0.0.1",
        "application": "Barz App",
        "text": "I am a unit test",
        "site": "heute",
    }) == "<137>@1622638021;20 horst|127.0.0.1 Barz App: I am a unit test\n"
