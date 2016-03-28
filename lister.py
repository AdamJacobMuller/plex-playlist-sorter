#!/usr/bin/python
import requests
import datetime
import time
import argparse
import json

import xml.etree.ElementTree as ET
#import lxml.etree as etree

parser = argparse.ArgumentParser()
parser.add_argument("--address", help="address of plex")
parser.add_argument("--playlist", help="playlist id")
args = parser.parse_args()

url = "%s/playlists/%s/items" % (args.address, args.playlist)
print url
items = requests.get(url)


items_xml = ET.fromstring(items.text.encode("ascii", errors="ignore"))

videos = items_xml.findall("./Video")

avt = []

for video in videos:
    #print json.dumps(video.attrib, indent=4)
    if 'grandparentTitle' in video.attrib:
        name = '%s - %s' % (video.attrib['grandparentTitle'], video.attrib['title'])
    else:
        name = '%s' % (video.attrib['title'])

    print "%s %s[%s]" % (video.attrib.get("originallyAvailableAt"), name, video.attrib['playlistItemID'])
