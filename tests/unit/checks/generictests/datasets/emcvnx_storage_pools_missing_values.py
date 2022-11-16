#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# fmt: off
# type: ignore

checkname = 'emcvnx_storage_pools'

info = [
    ['[[[storage_pools]]]'], ['Pool Name',
                               '  Pool 0'], ['Pool ID', '  0'],
    ['Raid Type', '  r_5'], ['Percent Full Threshold', '  70'],
    ['Description', '  '], ['Disk Type', '  SAS'], ['State', '  Ready'],
    ['Status', '  OK(0x0)'], ['Current Operation', '  None'],
    ['Current Operation State', '  N/A'],
    ['Current Operation Status', '  N/A'],
    ['Current Operation Percent Completed', '  0'],
    ['Raw Capacity (Blocks)', '  40527668736'],
    ['Raw Capacity (GBs)', '  19325.098'],
    ['User Capacity (Blocks)', '  35990175744'],
    ['User Capacity (GBs)', '  17161.453'],
    ['Consumed Capacity (Blocks)', '  20201398272'],
    ['Consumed Capacity (GBs)', '  9632.777'],
    ['Available Capacity (Blocks)', '  15788777472'],
    ['Available Capacity (GBs)', '  7528.676'],
    ['Percent Full', '  56.130'],
    ['LUN Allocation (Blocks)', '  19501416448'],
    ['LUN Allocation (GBs)', '  9299.000'],
    ['Snapshot Allocation (Blocks)', '  0'],
    ['Snapshot Allocation (GBs)', '  0.000'],
    ['Metadata Allocation (Blocks)', '  699981824'],
    ['Metadata Allocation (GBs)', '  333.777'],
    ['Total Subscribed Capacity (Blocks)', '  20201398272'],
    ['Total Subscribed Capacity (GBs)', '  9632.777'],
    ['Percent Subscribed', '  56.130'],
    ['Oversubscribed by (Blocks)', '  0'],
    ['Oversubscribed by (GBs)', '  0.000'],
    ['LUN Subscribed Capacity (Blocks)', '  19501416448'],
    ['LUN Subscribed Capacity (GBs)', '  9299.000'],
    ['Snapshot Subscribed Capacity (Blocks)', '  0'],
    ['Snapshot Subscribed Capacity (GBs)', '  0.000'],
    ['Metadata Subscribed Capacity (Blocks)', '  699981824'],
    ['Metadata Subscribed Capacity (GBs)', '  333.777'],
    ['Compression Savings (Blocks)', '  N/A'],
    ['Compression Savings (GBs)', '  N/A'], [''],
    ['Tier Name', '  Performance'], ['Raid Type', '  r_5'],
    ['Raid Drive Count', '  9'], ['User Capacity (GBs)', '  17161.45'],
    ['Consumed Capacity (GBs)', '  9632.78'],
    ['Available Capacity (GBs)', '  7528.68'],
    ['Percent Subscribed', '  56.13%'], ['Disks (Type)', ''],
    ['Bus 1 Enclosure 0 Disk 1 (SAS)'], ['Bus 1 Enclosure 0 Disk 8 (SAS)'],
    ['Bus 1 Enclosure 0 Disk 13 (SAS)'], ['Bus 0 Enclosure 1 Disk 10 (SAS)'],
    ['Bus 0 Enclosure 0 Disk 7 (SAS)'], ['Bus 0 Enclosure 0 Disk 9 (SAS)'],
    ['Bus 0 Enclosure 0 Disk 10 (SAS)'], ['Bus 0 Enclosure 0 Disk 12 (SAS)'],
    ['Bus 0 Enclosure 0 Disk 14 (SAS)'], ['Bus 0 Enclosure 1 Disk 1 (SAS)'],
    ['Bus 0 Enclosure 1 Disk 3 (SAS)'], ['Bus 0 Enclosure 1 Disk 5 (SAS)'],
    ['Bus 0 Enclosure 1 Disk 7 (SAS)'], ['Bus 0 Enclosure 1 Disk 9 (SAS)'],
    ['Bus 0 Enclosure 1 Disk 0 (SAS)'], ['Bus 1 Enclosure 0 Disk 10 (SAS)'],
    ['Bus 1 Enclosure 0 Disk 7 (SAS)'], ['Bus 1 Enclosure 0 Disk 9 (SAS)'],
    ['Bus 1 Enclosure 0 Disk 12 (SAS)'], ['Bus 1 Enclosure 0 Disk 3 (SAS)'],
    ['Bus 1 Enclosure 0 Disk 5 (SAS)'], ['Bus 0 Enclosure 0 Disk 6 (SAS)'],
    ['Bus 0 Enclosure 0 Disk 8 (SAS)'], ['Bus 0 Enclosure 1 Disk 2 (SAS)'],
    ['Bus 1 Enclosure 0 Disk 0 (SAS)'], ['Bus 1 Enclosure 0 Disk 11 (SAS)'],
    ['Bus 1 Enclosure 0 Disk 14 (Unknown)'],
    ['Bus 1 Enclosure 0 Disk 6 (SAS)'], ['Bus 1 Enclosure 0 Disk 2 (SAS)'],
    ['Bus 1 Enclosure 0 Disk 4 (SAS)'], ['Bus 0 Enclosure 0 Disk 11 (SAS)'],
    ['Bus 0 Enclosure 0 Disk 13 (SAS)'], ['Bus 0 Enclosure 1 Disk 4 (SAS)'],
    ['Bus 0 Enclosure 1 Disk 6 (SAS)'], ['Bus 0 Enclosure 1 Disk 8 (SAS)'],
    ['Bus 0 Enclosure 1 Disk 11 (SAS)'], [''],
    ['Rebalance Percent Complete', '  N/A'], ['Disks', ''],
    ['Bus 1 Enclosure 0 Disk 1'], ['Bus 1 Enclosure 0 Disk 13'],
    ['Bus 1 Enclosure 0 Disk 8'], ['Bus 0 Enclosure 1 Disk 10'],
    ['Bus 0 Enclosure 0 Disk 14'], ['Bus 0 Enclosure 0 Disk 12'],
    ['Bus 0 Enclosure 0 Disk 10'], ['Bus 0 Enclosure 0 Disk 9'],
    ['Bus 0 Enclosure 0 Disk 7'], ['Bus 0 Enclosure 1 Disk 9'],
    ['Bus 0 Enclosure 1 Disk 7'], ['Bus 0 Enclosure 1 Disk 5'],
    ['Bus 0 Enclosure 1 Disk 3'], ['Bus 0 Enclosure 1 Disk 1'],
    ['Bus 0 Enclosure 1 Disk 0'], ['Bus 1 Enclosure 0 Disk 10'],
    ['Bus 1 Enclosure 0 Disk 12'], ['Bus 1 Enclosure 0 Disk 9'],
    ['Bus 1 Enclosure 0 Disk 7'], ['Bus 1 Enclosure 0 Disk 5'],
    ['Bus 1 Enclosure 0 Disk 3'], ['Bus 0 Enclosure 0 Disk 8'],
    ['Bus 0 Enclosure 0 Disk 6'], ['Bus 0 Enclosure 1 Disk 2'],
    ['Bus 1 Enclosure 0 Disk 0'], ['Bus 1 Enclosure 0 Disk 11'],
    ['Bus 1 Enclosure 0 Disk 14'], ['Bus 1 Enclosure 0 Disk 6'],
    ['Bus 1 Enclosure 0 Disk 4'], ['Bus 1 Enclosure 0 Disk 2'],
    ['Bus 0 Enclosure 0 Disk 13'], ['Bus 0 Enclosure 0 Disk 11'],
    ['Bus 0 Enclosure 1 Disk 11'], ['Bus 0 Enclosure 1 Disk 8'],
    ['Bus 0 Enclosure 1 Disk 6'], ['Bus 0 Enclosure 1 Disk 4'],
    [
        'LUNs',
        '  136, 120, 111, 127, 131, 130, 121, 133, 102, 132, 103, 107, 126, 138, 137, 134, 105, 101, 109, 128, 122, 106, 129, 110, 123, 124, 135, 104, 100, 108, 125'
    ], ['FAST Cache', '  N/A'],
    ['Auto-Delete Pool Full Threshold Enabled', '  Off'],
    ['Auto-Delete Pool Full High Watermark', '  95.00'],
    ['Auto-Delete Pool Full Low Watermark', '  85.00'],
    ['Auto-Delete Pool Full State', '  Idle'],
    ['Auto-Delete Snapshot Space Used Threshold Enabled', '  Off'],
    ['Auto-Delete Snapshot Space Used High Watermark', '  25.00'],
    ['Auto-Delete Snapshot Space Used Low Watermark', '  20.00'],
    ['Auto-Delete Snapshot Space Used State',
     '  Idle'], [''], ['[[[auto_tiering]]]'],
    ['Auto-tiering is not supported on this system.'],
    ['Unrecognized option', ' (-info).']
]

discovery = {
    '': [('Pool 0', {})],
    'tiering': [('Pool 0', {})],
    'tieringtypes': [('Pool 0 Performance', {})],
    'deduplication': [('Pool 0', {})]
}

checks = {
    '': [
        (
            'Pool 0', {
                'percent_full': (70.0, 90.0)
            }, [
                (
                    0,
                    'State: Ready, Status: OK(0x0), [Phys. capacity] User capacity: 16.8 TiB, Consumed capacity: 9.41 TiB, Available capacity: 7.35 TiB',
                    []
                ), (0, 'Percent full: 56.13%', []),
                (
                    0,
                    '[Virt. capacity] Percent subscribed: 56.13%, Oversubscribed by: 0 B, Total subscribed capacity: 9.41 TiB',
                    [
                        (
                            'emcvnx_consumed_capacity', 10343115546165.248,
                            None, None, None, None
                        ),
                        (
                            'emcvnx_avail_capacity', 8083854300545.024, None,
                            None, None, None
                        ), ('emcvnx_perc_full', 56.13, None, None, None, None),
                        (
                            'emcvnx_perc_subscribed', 56.13, None, None, None,
                            None
                        ),
                        (
                            'emcvnx_over_subscribed', 0.0, None, None, None,
                            None
                        ),
                        (
                            'emcvnx_total_subscribed_capacity',
                            10343115546165.248, None, None, None, None
                        )
                    ]
                )
            ]
        )
    ],
    'tiering': [
        (
            'Pool 0', {
                'time_to_complete': (1814400, 2419200)
            }, [(0, 'Fast cache: N/A', [])]
        )
    ],
    'tieringtypes': [
        (
            'Pool 0 Performance', {}, [
                (0, 'User capacity: 16.8 TiB', []),
                (
                    0, 'Consumed capacity: 9.41 TiB', [
                        (
                            'emcvnx_consumed_capacity', 10343118767390.72,
                            None, None, None, None
                        )
                    ]
                ),
                (
                    0, 'Available capacity: 7.35 TiB', [
                        (
                            'emcvnx_avail_capacity', 8083858595512.32, None,
                            None, None, None
                        )
                    ]
                ),
                (
                    0, 'Percent subscribed: 56.13%', [
                        (
                            'emcvnx_perc_subscribed', 56.13, None, None, None,
                            None
                        )
                    ]
                )
            ]
        )
    ],
    'deduplication': [
        (
            'Pool 0', {}, [
                (0, 'State: unknown', []), (0, 'Status: unknown', []),
                (0, 'Rate: unknown', []),
                (0, 'Efficiency savings: unknown', []),
                (0, 'Percent completed: unknown', []),
                (0, 'Remaining size: unknown', []),
                (0, 'Shared capacity: unknown', [])
            ]
        )
    ]
}
