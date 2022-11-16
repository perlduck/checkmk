#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# fmt: off
# type: ignore

checkname = "fc_port"

info = [
    [
        '1',
        '10',
        '3',
        '9',
        '2000000',
        'port0',
        '7',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '2',
        '8',
        '2',
        '3',
        '2000000',
        'port1',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 50, 32, 70, 49, 32, 67, 50, 32, 70,
            51
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 50, 32, 65, 54, 32, 69, 57, 32, 67,
            50
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 49, 51, 32, 57, 66, 32, 67, 50, 32, 69, 54, 32, 57,
            52
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 49, 50, 32, 65, 69, 32, 56, 57, 32, 49, 48, 32, 65,
            67
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            54
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '3',
        '8',
        '2',
        '3',
        '2000000',
        'port2',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 52, 65, 32, 68, 50, 32, 49,
            68
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 49, 32, 51, 53, 32, 55, 52, 32, 52,
            55
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 49, 32, 55, 48, 32, 49, 55, 32, 48, 66, 32, 53,
            56
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 56, 32, 50, 57, 32, 51, 53, 32, 69, 56, 32, 69,
            56
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 50, 32, 51,
            65
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '4',
        '8',
        '2',
        '3',
        '2000000',
        'port3',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 49, 32, 53, 51, 32, 49, 54, 32, 54,
            52
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 49, 32, 56, 53, 32, 54, 57, 32, 50,
            69
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 67, 70, 32, 56, 68, 32, 51, 57, 32, 48,
            67
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 56, 32, 70, 52, 32, 57, 69, 32, 65, 53, 32, 52,
            52
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 69,
            65
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '5',
        '8',
        '2',
        '3',
        '2000000',
        'port4',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 51, 32, 52, 52, 32, 54, 56, 32, 65,
            65
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 50, 32, 70, 53, 32, 69, 68, 32, 56,
            54
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 52, 32, 70, 52, 32, 53, 48, 32, 51, 70, 32, 53,
            56
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 70, 32, 68, 69, 32, 68, 50, 32, 52, 50, 32, 69,
            56
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 54, 32, 54,
            53
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '6',
        '8',
        '2',
        '3',
        '2000000',
        'port5',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 68, 65, 32, 56, 52, 32, 49,
            53
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 50, 32, 48, 70, 32, 70, 51, 32, 51,
            65
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 51, 32, 56, 56, 32, 56, 65, 32, 53, 52, 32, 49,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 69, 32, 70, 65, 32, 55, 67, 32, 55, 53, 32, 54,
            56
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 51, 32, 57,
            70
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '7',
        '8',
        '2',
        '3',
        '2000000',
        'port6',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 53, 48, 32, 68, 65, 32, 50,
            51
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 51, 66, 32, 70, 54, 32, 51,
            68
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 49, 69, 32, 57, 49, 32, 67, 55, 32, 48,
            52
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 56, 68, 32, 49, 51, 32, 54, 70, 32, 70,
            67
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '8',
        '8',
        '2',
        '3',
        '2000000',
        'port7',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 52, 66, 32, 48, 65, 32, 54,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 50, 69, 32, 66, 51, 32, 49,
            55
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 49, 68, 32, 52, 49, 32, 66, 67, 32, 51,
            56
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 51, 55, 32, 70, 67, 32, 65, 54, 32, 54,
            52
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            51
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '9',
        '10',
        '3',
        '9',
        '2000000',
        'port8',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '10',
        '10',
        '3',
        '9',
        '2000000',
        'port9',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '11',
        '10',
        '3',
        '9',
        '2000000',
        'port10',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '12',
        '10',
        '3',
        '9',
        '2000000',
        'port11',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '13',
        '10',
        '3',
        '9',
        '2000000',
        'port12',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '14',
        '10',
        '3',
        '9',
        '2000000',
        'port13',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '15',
        '10',
        '3',
        '9',
        '2000000',
        'port14',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '16',
        '10',
        '3',
        '9',
        '2000000',
        'port15',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '17',
        '10',
        '3',
        '9',
        '2000000',
        'port16',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '18',
        '9',
        '2',
        '3',
        '2000000',
        'port17',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 50, 32, 50, 66, 32, 56, 54, 32, 57,
            52
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 53, 70, 32, 56, 65, 32, 66,
            69
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 49, 49, 32, 57, 66, 32, 54, 55, 32, 57, 56, 32, 56,
            67
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 54, 52, 32, 50, 50, 32, 56, 57, 32, 52,
            52
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 53, 32, 67, 68, 32, 50,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '19',
        '9',
        '2',
        '3',
        '2000000',
        'port18',
        '4',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 55, 32, 56, 52, 32, 49, 57, 32, 68,
            68
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 53, 32, 67, 56, 32, 52, 49, 32, 51,
            49
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 51, 49, 32, 68, 57, 32, 53, 49, 32, 53, 69, 32, 48,
            52
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 49, 68, 32, 54, 53, 32, 70, 65, 32, 48, 56, 32, 51,
            67
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 53, 32, 67, 68, 32, 50,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '20',
        '10',
        '3',
        '9',
        '2000000',
        'port19',
        '7',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '21',
        '10',
        '3',
        '9',
        '2000000',
        'port20',
        '7',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '22',
        '10',
        '3',
        '9',
        '2000000',
        'port21',
        '7',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '23',
        '10',
        '3',
        '9',
        '2000000',
        'port22',
        '7',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
    [
        '24',
        '10',
        '3',
        '9',
        '2000000',
        'port23',
        '7',
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
        [
            48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48, 48, 32, 48,
            48
        ],
    ],
]

discovery = {
    '': [
        ('01', 'fc_port_default_levels'),
        ('02', 'fc_port_default_levels'),
        ('03', 'fc_port_default_levels'),
        ('04', 'fc_port_default_levels'),
        ('05', 'fc_port_default_levels'),
        ('06', 'fc_port_default_levels'),
        ('07', 'fc_port_default_levels'),
        ('17', 'fc_port_default_levels'),
        ('18', 'fc_port_default_levels'),
    ],
}

DEFAULT_PARAMS = {
    "rxcrcs": (3.0, 20.0),  # allowed percentage of CRC errors
    "rxencoutframes": (3.0, 20.0),  # allowed percentage of Enc-OUT Frames
    "notxcredits": (3.0, 20.0),  # allowed percentage of No Tx Credits
    "c3discards": (3.0, 20.0),  # allowed percentage of C3 discards
}

checks = {
    '': [('01', DEFAULT_PARAMS, [
        (0, '16.0 Gbit/s, In: 0.00 B/s, Out: 0.00 B/s, online, ready, active, f-port', [
            ('in', 0.0, None, None, 0, 2000000000.0),
            ('out', 0.0, None, None, 0, 2000000000.0),
            ('rxobjects', 0.0),
            ('txobjects', 0.0),
            ('rxcrcs', 0.0),
            ('rxencoutframes', 0.0),
            ('c3discards', 0.0),
            ('notxcredits', 0.0),
        ]),
    ]),],
}
