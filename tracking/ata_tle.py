#!/usr/bin/env python3
import sys
from ATATools.ata_control import *
tle=sys.argv[1]
antstr=sys.argv[2]

f = open(tle)
l1 = f.readline()

status=make_and_track_tle(tle, antstr)
print(status.decode("utf-8") )
