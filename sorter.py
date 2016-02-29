#!/usr/bin/python
import requests
import datetime
import time
import argparse
import json

import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser()
parser.add_argument("--address", help="address of plex")
parser.add_argument("--playlist", help="playlist id")
args = parser.parse_args()

url = "%s/playlists/%s/items" % (args.address, args.playlist)
items = requests.get(url)


items_xml = ET.fromstring(items.text.encode("ascii", errors="ignore"))

videos = items_xml.findall("./Video")

avt = []

for video in videos:
    if 'originallyAvailableAt' not in video.attrib:
        print json.dumps(video.attrib, indent=4)
        continue
    avt.append((time.mktime(datetime.datetime.strptime(video.attrib['originallyAvailableAt'], "%Y-%m-%d").timetuple()), video.attrib['playlistItemID']))

avts = sorted(avt, key=lambda tup: tup[0])

last = None
for avt in avts:
    if last is None:
        requests.put("%s/playlists/%s/items/%s/move" % (args.address, args.playlist, avt[1]))
        print("moving %s to top" % avt[1])
        last = avt[1]
    else:
        requests.put("%s/playlists/%s/items/%s/move?after=%s" % (args.address, args.playlist, avt[1], last))
        print("moving %s after %s" % (avt[1], last))
        last = avt[1]
