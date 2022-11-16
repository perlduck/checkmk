#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# fmt: off
# type: ignore

checkname = 'msexch_isclienttype'

info = [
    [
        'AdministrativeRPCrequestsPersec', 'AdminRPCRequests', 'Caption', 'Description',
        'DirectoryAccessLDAPSearchesPersec', 'Frequency_Object', 'Frequency_PerfTime',
        'Frequency_Sys100NS', 'JetLogRecordBytesPersec', 'JetLogRecordsPersec',
        'JetPagesModifiedPersec', 'JetPagesPrereadPersec', 'JetPagesReadPersec',
        'JetPagesReferencedPersec', 'JetPagesRemodifiedPersec', 'LazyindexescreatedPersec',
        'LazyindexesdeletedPersec', 'LazyindexfullrefreshPersec',
        'LazyindexincrementalrefreshPersec', 'MessagescreatedPersec', 'MessagesdeletedPersec',
        'MessagesopenedPersec', 'MessagesupdatedPersec', 'Name', 'PropertypromotionsPersec',
        'RPCAverageLatency', 'RPCAverageLatency_Base', 'RPCBytesReceivedPersec',
        'RPCBytesSentPersec', 'RPCOperationsPersec', 'RPCPacketsPersec', 'RPCRequests',
        'Timestamp_Object', 'Timestamp_PerfTime', 'Timestamp_Sys100NS'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'hrc', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'officegraph', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
        'publicfolderhierarchyreplication', '0', '0', '0', '0', '0', '0', '0', '0', '0',
        '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'unifiedauditing', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'snackyservice', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'addriver', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'liveidbasicauth', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'pop', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'notificationbroker', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '958', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'unifiedpolicy', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'outlookservice', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'mailboxloadbalance', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'anchorservice', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0',
        'contentindexingmovedestination', '0', '0', '0', '0', '0', '0', '0', '0', '0',
        '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'ediscoverysearch', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'publicfoldersystem', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '11495', '0', '', '', '22627', '0', '1953125', '10000000', '540', '6', '1', '0',
        '0', '23098', '3', '0', '0', '0', '0', '0', '0', '0', '0', 'simplemigration',
        '0', '69283', '126447', '0', '43957144', '287377', '126447', '11495', '0',
        '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'loadgen', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '59353', '0', '', '', '4311', '0', '1953125', '10000000', '1740', '18', '0',
        '8', '10', '3388915', '12', '0', '0', '0', '0', '0', '0', '0', '0',
        'storeactivemonitoring', '0', '176465', '574334', '0', '331274072', '1033798',
        '574334', '57433', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'teammailbox', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'sms', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'inference', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '183763', '0', '', '', '88', '0', '1953125', '10000000', '50065286', '2423113',
        '5244', '434', '135', '3750983', '1679627', '0', '24', '0', '80', '0', '0', '0',
        '0', 'maintenance', '0', '0', '0', '0', '0', '0', '0', '0', '0',
        '6743176285319', '130951777565340000'
    ],
    [
        '86269', '0', '', '', '2', '0', '1953125', '10000000', '66', '3', '1', '0',
        '4', '311', '1', '0', '0', '0', '0', '0', '0', '0', '0', 'ha', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'transportsync', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '55887', '0', '', '', '108', '0', '1953125', '10000000', '580', '6', '0', '0',
        '0', '108', '4', '0', '0', '0', '0', '0', '0', '0', '0', 'migration', '0',
        '8668', '49818', '0', '3645017', '141151', '49818', '8303', '0', '6743176285319',
        '130951777565340000'
    ],
    [
        '0', '0', '', '', '10413', '0', '1953125', '10000000', '23651', '210', '0', '4',
        '1', '22859226', '140', '0', '0', '0', '0', '0', '0', '0', '0', 'momt', '0',
        '524761', '1148614', '0', '1301595880', '2067486', '1148614', '114863', '0',
        '6743176285319', '130951777565340000'
    ],
    [
        '41455', '0', '', '', '1589', '0', '1953125', '10000000', '20909367', '639566',
        '1293', '380', '92', '3712279', '427309', '0', '0', '0', '752', '0', '2', '100',
        '96', 'timebasedassistants', '0', '53399', '29902', '1040', '27396903', '72740',
        '29902', '1060', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'approvalapi', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'webservices', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'unifiedmessaging', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '11502', '0', '', '', '7091', '0', '1953125', '10000000', '125279633', '1345068',
        '10501', '0', '18', '1925947', '1016274', '0', '0', '0', '0', '23004', '0',
        '11502', '23004', 'monitoring', '0', '304479', '897860', '0', '160522104',
        '1012880', '897860', '165768', '0', '6743176285319', '130951777565340000'
    ],
    [
        '22857', '0', '', '', '28', '0', '1953125', '10000000', '5249', '131', '12',
        '0', '3', '427880', '77', '1', '0', '1', '4', '0', '0', '4', '0', 'management',
        '0', '623', '280', '0', '208125', '669', '280', '15', '0', '6743176285319',
        '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'elc', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'availabilityservice', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '3419753', '0', '', '', '1898', '0', '1953125', '10000000', '293', '7', '0',
        '0', '2', '948423', '4', '0', '0', '0', '0', '0', '0', '35747', '0',
        'contentindexing', '0', '103789', '72246', '0', '202073477', '123630', '72246',
        '1093', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'rpchttp', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'imap', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'owa', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '8903712', '0', '', '', '2421', '0', '1953125', '10000000', '146072449',
        '4829076', '537', '0', '8', '12336816', '3218853', '0', '0', '0', '0', '0', '0',
        '202', '0', 'eventbasedassistants', '0', '4017', '2568', '0', '2752073', '6242',
        '2568', '108', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '10096', '0', '1953125', '10000000', '71226', '808', '80',
        '0', '2', '1604', '544', '0', '0', '0', '0', '0', '0', '19165', '40',
        'airsync', '0', '113736', '76832', '0', '49952360', '172924', '76832', '1', '0',
        '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '618', '0', '1953125', '10000000', '272223148', '2854731',
        '31380', '0', '37', '4065273', '2163330', '2', '0', '2', '2', '57482', '23004',
        '34506', '0', 'transport', '0', '543742', '529138', '0', '424193667', '1219430',
        '529138', '40243', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'user', '0', '926',
        '400382', '0', '0', '0', '400382', '400382', '0', '6743176285319',
        '130951777565340000'
    ],
    [
        '406299', '0', '', '', '98', '0', '1953125', '10000000', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'administrator', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '6743176285319', '130951777565340000'
    ],
    [
        '0', '0', '', '', '0', '0', '1953125', '10000000', '0', '0', '0', '0', '0',
        '0', '0', '0', '0', '0', '0', '0', '0', '0', '0', 'system', '0', '0', '3',
        '0', '0', '0', '3', '345025', '0', '6743176285319', '130951777565340000'
    ],
    [
        '13203303', '0', '', '', '61388', '0', '1953125', '10000000', '614653228',
        '12092743', '49049', '826', '312', '53440863', '8506178', '3', '24', '3', '838',
        '80486', '23006', '101226', '23140', '_total', '0', '1903888', '3908424', '1040',
        '400087174', '6138327', '3908424', '1145789', '0', '6743176285319',
        '130951777565340000'
    ]
]

discovery = {
    '': [('_total', None), ('addriver', None), ('administrator', None), ('airsync', None),
         ('anchorservice', None), ('approvalapi', None), ('availabilityservice', None),
         ('contentindexing', None), ('contentindexingmovedestination', None),
         ('ediscoverysearch', None), ('elc', None), ('eventbasedassistants', None), ('ha',
                                                                                        None),
         ('hrc', None), ('imap', None), ('inference', None), ('liveidbasicauth', None),
         ('loadgen', None), ('mailboxloadbalance', None), ('maintenance', None),
         ('management', None), ('migration', None), ('momt', None), ('monitoring', None),
         ('notificationbroker', None), ('officegraph', None), ('outlookservice', None),
         ('owa', None), ('pop', None), ('publicfolderhierarchyreplication', None),
         ('publicfoldersystem', None), ('rpchttp', None), ('simplemigration', None),
         ('sms', None), ('snackyservice', None), ('storeactivemonitoring', None),
         ('system', None), ('teammailbox', None), ('timebasedassistants', None),
         ('transport', None), ('transportsync', None), ('unifiedauditing', None),
         ('unifiedmessaging', None), ('unifiedpolicy', None), ('user', None),
         ('webservices', None)]
}

checks = {
    '': [('_total', {
        'store_latency': {
            'upper': (40.0, 50.0)
        },
        'clienttype_requests': {
            'upper': (60, 70)
        },
        'clienttype_latency': {
            'upper': (40.0, 50.0)
        }
    }, [(0, 'Average latency: 0.49 ms', [('average_latency', 0.48712422193702626, 40.0, 50.0, None,
                                        None)]),
        (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('addriver', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('administrator', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('airsync', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 2.6480752376567898e-05, 40.0, 50.0,
                                             None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('anchorservice', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('approvalapi', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('availabilityservice', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('contentindexing', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 2.4164853195197893e-05, 40.0, 50.0,
                                             None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('contentindexingmovedestination', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('ediscoverysearch', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('elc', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
             }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('eventbasedassistants', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 9.352801363450964e-07, 40.0, 50.0,
                                             None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('ha', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('hrc', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('imap', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('inference', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('liveidbasicauth', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('loadgen', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('mailboxloadbalance', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('maintenance', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('management', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 1.4505348153995004e-07, 40.0, 50.0,
                                             None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('migration', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.17 ms', [('average_latency', 0.17399333574210124, 40.0, 50.0,
                                             None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('momt', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.46 ms', [('average_latency', 0.45686453412547645, 40.0, 50.0,
                                             None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('monitoring', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.34 ms', [('average_latency', 0.33911634330519236, 40.0, 50.0,
                                             None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('notificationbroker', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('officegraph', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('outlookservice', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('owa', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('pop', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('publicfolderhierarchyreplication', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('publicfoldersystem', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('rpchttp', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('simplemigration', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.55 ms', [('average_latency', 0.5479212634542535, 40.0, 50.0,
                                             None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('sms', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('snackyservice', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('storeactivemonitoring', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.31 ms', [('average_latency', 0.3072515295977602, 40.0, 50.0,
                                             None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('system', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('teammailbox', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('timebasedassistants', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 1.243283698179493e-05, 40.0, 50.0,
                                             None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('transport', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0001265842047257069, 40.0, 50.0,
                                             None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('transportsync', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('unifiedauditing', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('unifiedmessaging', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('unifiedpolicy', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('user', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0023127912843234713, 40.0, 50.0,
                                             None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])]),
         ('webservices', {
             'store_latency': {
                 'upper': (40.0, 50.0)
             },
             'clienttype_requests': {
                 'upper': (60, 70)
             },
             'clienttype_latency': {
                 'upper': (40.0, 50.0)
             }
         }, [(0, 'Average latency: 0.00 ms', [('average_latency', 0.0, 40.0, 50.0, None, None)]),
             (0, 'RPC Requests/sec: 0.00', [('requests_per_sec', 0.0, 60, 70, None, None)])])]
}
