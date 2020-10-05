#!/usr/bin/env python3
import sys
from ATATools.ata_control import *
antstr=sys.argv[1]
freq=float(sys.argv[2])

status=set_freq(freq, antstr.split(','), lo='d')

print(status)
