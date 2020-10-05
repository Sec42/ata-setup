#!/usr/bin/env python3
import sys
from ATATools.ata_control import *
az=sys.argv[1]
el=sys.argv[2]
antstr=sys.argv[3]

status=set_az_el(antstr, float(az), float(el))
print(status.decode("utf-8") )
