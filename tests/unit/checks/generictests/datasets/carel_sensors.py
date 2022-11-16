#!/usr/bin/env python3
# Copyright (C) 2019 tribe29 GmbH - License: GNU General Public License v2
# This file is part of Checkmk (https://checkmk.com). It is subject to the terms and
# conditions defined in the file COPYING, which is part of this source code package.

# fmt: off
# type: ignore


checkname = 'carel_sensors'

info = [
    ['1.0', '264'], ['2.0', '0'], ['3.0', '221'], ['4.0', '0'],
    ['5.0', '0'], ['6.0', '0'], ['7.0', '0'], ['8.0', '0'],
    ['9.0', '0'], ['10.0', '0'], ['11.0', '0'], ['12.0', '0'],
    ['13.0', '0'], ['14.0', '0'], ['15.0', '0'], ['16.0', '491'],
    ['17.0', '0'], ['18.0', '497'], ['19.0', '0'], ['20.0', '220'],
    ['21.0', '150'], ['22.0', '0'], ['23.0', '170'], ['24.0', '0'],
    ['25.0', '15'], ['26.0', '40'], ['27.0', '10'], ['28.0', '280'],
    ['29.0', '160'], ['30.0', '70'], ['31.0', '200'], ['32.0', '70'],
    ['33.0', '80'], ['34.0', '280'], ['35.0', '14'], ['36.0', '20'],
    ['37.0', '3'], ['38.0', '0'], ['39.0', '0'], ['40.0', '2640'],
    ['41.0', '0'], ['42.0', '0'], ['43.0', '2200'], ['44.0', '1700'],
    ['45.0', '0'], ['46.0', '0'], ['47.0', '0'], ['48.0', '0'],
    ['49.0', '0'], ['50.0', '0'], ['51.0', '0'], ['52.0', '0'],
    ['53.0', '0'], ['54.0', '0'], ['55.0', '0'], ['56.0', '0'],
    ['57.0', '0'], ['58.0', '0'], ['59.0', '0'], ['60.0', '0'],
    ['61.0', '0'], ['62.0', '0'], ['63.0', '0'], ['64.0', '0'],
    ['65.0', '0'], ['66.0', '0'], ['67.0', '0'], ['68.0', '0'],
    ['69.0', '0'], ['70.0', '350'], ['71.0', '200'], ['72.0', '1000'],
    ['73.0', '150'], ['74.0', '220'], ['75.0', '180'], ['76.0', '200'],
    ['77.0', '491'], ['78.0', '150'], ['79.0', '0'], ['80.0', '0'],
    ['81.0', '263'], ['82.0', '0'], ['83.0', '0'], ['84.0', '0'],
    ['85.0', '0'], ['86.0', '-50'], ['87.0', '50'], ['88.0', '-159'],
    ['89.0', '750'], ['90.0', '850'], ['91.0', '498'], ['92.0', '0'],
    ['93.0', '-500'], ['94.0', '0'], ['95.0', '0'], ['96.0', '0'],
    ['97.0', '0'], ['98.0', '0'], ['99.0', '0'], ['100.0', '0'],
    ['101.0', '0'], ['102.0', '0'], ['103.0', '-500'],
    ['104.0', '230'], ['105.0', '158'], ['106.0', '0'], ['107.0', '0'],
    ['108.0', '0'], ['109.0', '0'], ['110.0', '0'], ['111.0', '0'],
    ['112.0', '0'], ['113.0', '0'], ['114.0', '0'], ['115.0', '0'],
    ['116.0', '0'], ['117.0', '0'], ['118.0', '0'], ['119.0', '0'],
    ['120.0', '0'], ['121.0', '0'], ['122.0', '0'], ['123.0', '0'],
    ['124.0', '0'], ['125.0', '0'], ['126.0', '0'], ['127.0', '0'],
    ['128.0', '-858993460'], ['129.0', '-858993460'],
    ['130.0', '-858993460'], ['131.0', '-858993460'],
    ['132.0', '-858993460'], ['133.0', '-858993460'],
    ['134.0', '-858993460'], ['135.0', '-858993460'],
    ['136.0', '-858993460'], ['137.0', '-858993460'],
    ['138.0', '-858993460'], ['139.0', '-858993460'],
    ['140.0', '-858993460'], ['141.0', '-858993460'],
    ['142.0', '-858993460'], ['143.0', '-858993460'],
    ['144.0', '-858993460'], ['145.0', '-858993460'],
    ['146.0', '-858993460'], ['147.0', '-858993460'],
    ['148.0', '-858993460'], ['149.0', '-858993460'],
    ['150.0', '-858993460'], ['151.0', '-858993460'],
    ['152.0', '-858993460'], ['153.0', '-858993460'],
    ['154.0', '-858993460'], ['155.0', '-858993460'],
    ['156.0', '-858993460'], ['157.0', '-858993460'],
    ['158.0', '-858993460'], ['159.0', '-858993460'],
    ['160.0', '-858993460'], ['161.0', '-858993460'],
    ['162.0', '-858993460'], ['163.0', '-858993460'],
    ['164.0', '-858993460'], ['165.0', '-858993460'],
    ['166.0', '-858993460'], ['167.0', '-858993460'],
    ['168.0', '-858993460'], ['169.0', '-858993460'],
    ['170.0', '-858993460'], ['171.0', '-858993460'],
    ['172.0', '-858993460'], ['173.0', '-858993460'],
    ['174.0', '-858993460'], ['175.0', '-858993460'],
    ['176.0', '-858993460'], ['177.0', '-858993460'],
    ['178.0', '-858993460'], ['179.0', '-858993460'],
    ['180.0', '-858993460'], ['181.0', '-858993460'],
    ['182.0', '-858993460'], ['183.0', '-858993460'],
    ['184.0', '-858993460'], ['185.0', '-858993460'],
    ['186.0', '-858993460'], ['187.0', '-858993460'],
    ['188.0', '-858993460'], ['189.0', '-858993460'],
    ['190.0', '-858993460'], ['191.0', '-858993460'],
    ['192.0', '-858993460'], ['193.0', '-858993460'],
    ['194.0', '-858993460'], ['195.0', '-858993460'],
    ['196.0', '-858993460'], ['197.0', '-858993460'],
    ['198.0', '-858993460'], ['199.0', '-858993460'],
    ['200.0', '-858993460'], ['201.0', '-858993460'],
    ['202.0', '-858993460'], ['203.0', '-858993460'],
    ['204.0', '-858993460'], ['205.0', '-858993460'],
    ['206.0', '-858993460'], ['207.0', '-858993460']
]

discovery = {
    '': [
        ('Cooling Prop. Band', {
            'levels': (60, 70)
        }), ('Cooling Set Point', {
            'levels': (60, 70)
        }), ('Delivery', {
            'levels': (60, 70)
        }), ('Heating Prop. Band', {
            'levels': (60, 70)
        }), ('Heating Set Point', {
            'levels': (60, 70)
        }), ('Room', {
            'levels': (30, 35)
        })
    ]
}

checks = {
    '': [
        (
            'Cooling Prop. Band', {
                'levels': (60, 70)
            }, [(0, '15.0 \xb0C', [('temp', 15.0, 60, 70, None, None)])]
        ),
        (
            'Cooling Set Point', {
                'levels': (60, 70)
            }, [(0, '22.0 \xb0C', [('temp', 22.0, 60, 70, None, None)])]
        ),
        (
            'Delivery', {
                'levels': (60, 70)
            }, [(0, '22.1 \xb0C', [('temp', 22.1, 60, 70, None, None)])]
        ),
        (
            'Heating Prop. Band', {
                'levels': (60, 70)
            }, [(0, '1.5 \xb0C', [('temp', 1.5, 60, 70, None, None)])]
        ),
        (
            'Heating Set Point', {
                'levels': (60, 70)
            }, [(0, '17.0 \xb0C', [('temp', 17.0, 60, 70, None, None)])]
        ),
        (
            'Room', {
                'levels': (30, 35)
            }, [(0, '26.4 \xb0C', [('temp', 26.4, 30, 35, None, None)])]
        )
    ]
}
