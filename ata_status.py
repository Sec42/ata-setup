#!/usr/bin/env python3
from ATATools.ata_control import *
status=get_ascii_status()

print(status.decode("utf-8") )
