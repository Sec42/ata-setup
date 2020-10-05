#!/usr/bin/env python3
import sys
from ATATools.ata_control import *
antstr=sys.argv[1]
atten=float(sys.argv[2])

if atten<20:
    raise Exception("atten needs to be >=20, please")

if atten>31.5:
    raise Exception("atten max is 31.5")

antlist=[]
freqlist=[]
for ant in antstr.split(','):
    antlist.append("%sx"%ant)
    freqlist.append(atten)
    antlist.append("%sy"%ant)
    freqlist.append(atten)

print(antlist,freqlist)

status=set_atten_thread([antlist],[freqlist])
print(status)
