#!/usr/bin/python
import os, sys, re, urllib
radio = int(sys.argv[1])
# Get a file-like object for the Python Web site's home page.
f = urllib.urlopen("http://sc.studioclassroom.com/Sc-rD.php")
# Read from the object, storing the page's contents in 's'.
s = f.read()
f.close()
#print s
#obj = re.findall(r'href[\s]+=[\s]+\"(mms://203.69.69.81/[\s\S]+?baa[\s\S]+?\.wma).*?\">', s)
obj = re.findall(r'href[\s]+=[\s]+?\"(mms://203.69.69.81/.+?baa.+?\.wma)\">?', s)
for i in range(len(obj)):
    obj[i] = obj[i].replace("mms","http")
    print i, obj[i]

if radio <= range(len(obj)):
    os.system("mplayer -prefer-ipv4 -cache 128 -ao alsa:noblock:device=hw=1.0 %s"%obj[radio])
else:
    os.system("mplayer -prefer-ipv4 -cache 128 -ao alsa:noblock:device=hw=1.0 %s"%obj[0])
