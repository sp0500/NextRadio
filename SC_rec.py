#!/usr/bin/python
import os, sys, re, urllib

today = os.popen('date +%Y%m%d').read().rstrip("\n")


f = urllib.urlopen("http://lt.studioclassroom.com/LT-RaDio.php")
s = f.read()
f.close()
obj = re.findall(r'href[\s]+=[\s]+\"(mms://203.69.69.81/[\s\S]+?lta[\s\S]+?\.wma)', s)
if obj:
    os.system("mimms -q %s %s_lta.wma"%(obj[0],today))

f = urllib.urlopen("http://sc.studioclassroom.com/Sc-rD.php")
s = f.read()
f.close()
obj = re.findall(r'href[\s]+=[\s]+?\"(mms://203.69.69.81/.+?baa.+?\.wma)\">?', s)
if obj:
    os.system("mimms -q %s %s_baa.wma"%(obj[0],today))

f = urllib.urlopen("http://ad.studioclassroom.com/Ad-RAd.php")
s = f.read()
f.close()
obj = re.findall(r'href[\s]+=[\s]+?\"(mms://203.69.69.81/.+?ada.+?\.wma)\">?', s)
if obj:
    os.system("mimms -q %s %s_ada.wma"%(obj[0],today))

