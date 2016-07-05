#!/usr/bin/env python
'''
Test for connection status of each channel

This is a bit messy, should redo parser
Also should probably use urllib2 (vs. requests) for consistency with addon, although hopefully shouldn't matter
TODO Need to test Sonica and Radio3

'''

import sys
import os.path
import requests

CUR_DIR = os.path.dirname(__file__)
RESOURCES_DIR = os.path.abspath(os.path.join(CUR_DIR, os.path.pardir, 'resources', 'lib'))
sys.path.append(RESOURCES_DIR)

import CBCJsonParser

'''
Checks that it is possible to connect to the stream specified by region and channel

Args:
    region: The region served by channel
    channel: radio1 or radio2
    qual: 0 for High, 1 for Low
'''
def checkRegionConnection(region, channel, qual=0):
    if channel == "radio1":
        url = CBCJsonParser.parse_pls(CBCJsonParser.get_R1_streams(region)[qual])
    elif channel == "radio2":
        url = CBCJsonParser.parse_pls(CBCJsonParser.get_R2_streams(region))

    try:
        r = requests.head(url)
        if r.status_code < 400:
            print("Success: Connection to HQ R1 stream for: " + region)
        else:
            print("Cannot access stream for: " + region)
    except (requests.ConnectionError, requests.Timeout):
        print("Connection error to server")

if __name__ == "__main__":
    # Radio 1 High quality check
    for region in CBCJsonParser.get_regions('radio1'):
        checkRegionConnection(region, 'radio1', 0)

    # Radio 1 Low quality check
    for region in CBCJsonParser.get_regions('radio1'):
        checkRegionConnection(region, 'radio1', 1)

    # Radio 2 check
    for region in CBCJsonParser.get_regions('radio2'):
        checkRegionConnection(region, 'radio2')
