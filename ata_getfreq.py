#!/usr/bin/env python3
import sys
from ATATools.ata_control import *
antstr=sys.argv[1]

status=get_freq(antstr.split(','), lo='d')

for ant in status:
    print ("%s: LO=%f focus=%f"%(ant,status[ant][0],status[ant][1]))
