#!/usr/bin/python
#-*- coding: utf-8 -*-
#############################################
#
# Python script for NextRadio (a.py)
# Version: 1.1
#
# Created by Aladdin
#
# Changes Logs:
# [2013-04-20] By A-Lang
#              Replaced the lircrc with the mplayer's subordinate mode
#              Added the audio volume control
#              Added the Mute,Power keys function
#
# [2013-04-22] By Aladdin
#              Sky.FM and BBC Radio supported
#              Reorganized
#              Enabled IR keys Play,Favor,Home

import socket, re, os, subprocess, time, urllib
from subprocess import Popen, PIPE

def Say_station(st):
    audio_dir = "/root/NextRadio/sounds"
    prompt ="" 

    ip_string = str(st)
    for digit in ip_string:
        prompt = "%s /root/NextRadio/sounds/%s.wav" %(prompt,digit)

    #os.system("mplayer -ao oss -quiet " + prompt + " < /dev/null  ")
    return prompt

def PlayRadio(station):
    print station, stationlist[station]
    os.system("killall " + "mplayer");
    prompt = Say_station(station)
    #Say_station(station)
    time.sleep(1)
    if 'pls' in stationlist[station] or 'asx' in stationlist[station]:
        Play_station = "mplayer -ao oss -subordinate -quiet -cache 256 " + "-loop 0 " + "-cache-min 10" + prompt + " -playlist " + stationlist[station].rstrip("\n") + " < /dev/null &"
    else:
        Play_station = "mplayer -ao oss -subordinate -quiet -cache 256 " + "-loop 0 " + "-cache-min 10" + prompt + " " + stationlist[station].rstrip("\n") + " < /dev/null &"
    print Play_station
    player = subprocess.Popen(Play_station.split(" "), stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return player

def ReadKey():
    funckey = 0
    while 1:
        data = client_socket.recv(512)
        cmd_list = data.split( " " )
        if (cmd_list[1] == "00"):
            if (cmd_list[2][0] == 'D'):
                return funckey + int (cmd_list[2][1])
            elif (cmd_list[2][0] == 'R'):
                funckey = funckey + 10
            elif (cmd_list[2][0] == 'G'):
                funckey = funckey + 20
            elif (cmd_list[2][0] == 'Y'):
                funckey = funckey + 30
            elif (cmd_list[2][0] == 'B'):
                funckey = funckey + 40
            elif (cmd_list[2] == "power"):
                return 2000
            elif (cmd_list[2] == "chUp" or cmd_list[2] == "chUp_V2"):
                return 1000
            elif (cmd_list[2] == "chDown" or cmd_list[2] == "chDown_V2"):
                return 1001
            elif (cmd_list[2] == "volUp" or cmd_list[2] == "volUp_V2"):
                return 1002
            elif (cmd_list[2] == "volDown" or cmd_list[2] == "volDown_V2"):
                return 1003
            elif (cmd_list[2] == "mute"):
                return 1004
            elif (cmd_list[2] == "play"):
                return 1005
            elif (cmd_list[2] == "favor"): # set favor station
                return 1006
            elif (cmd_list[2] == "home"): # play favor station
                return 1007


i = 0
stationlist=[]
funkey = 0
power = 1
max_stations = 0
current_station = 0
sockfile = '/dev/lircd'

# Get LTE
f = urllib.urlopen("http://aladdinsip.no-ip.org/sc.html")
#f = urllib.urlopen("http://lt.studioclassroom.com/LT-RaDio.php")
s = f.read()
f.close()
obj_lta = re.findall(r'(mms://203.69.69.81/studio/[0-9]+lta.+?\.wma)', s)
if (obj_lta):
    print 'Lta = ', obj_lta
    for j in range (3):
        obj_lta[j] = obj_lta[j].replace("mms","http")
        stationlist.append(obj_lta[j])
        i = i + 1

obj_baa = re.findall(r'(mms://203.69.69.81/studio/[0-9]+?baa.+?\.wma)', s)
if (obj_baa):
    print 'Baa = ', obj_baa
    for j in range (3):
        obj_baa[j] = obj_baa[j].replace("mms","http")
        stationlist.append(obj_baa[j])
        i = i + 1

obj_ada = re.findall(r'(mms://203.69.69.81/studio/[0-9]+?ada.+?\.wma)', s)
if (obj_ada):
    print 'Ada = ', obj_ada
    for j in range (3):
        obj_ada[j] = obj_ada[j].replace("mms","http")
        stationlist.append(obj_ada[j])
        i = i + 1


stationlist.append(obj_baa[0])
print stationlist

today = os.popen('date +%Y%m%d').read()
print today

fd = open ("/root/NextRadio/all.pls","r")
for line in fd:
    msg = re.search('^#',line)
    if msg:
       pass
    else:
       stationlist.append(line)
       i = i+1
fd.close()

max_stations = i-1

if os.path.exists('/root/NextRadio/favor.txt'):
    fd = open ('/root/NextRadio/favor.txt')
    favor = int(fd.readline())
    fd.close()
else:
    favor = 0 
current_station = favor
player = PlayRadio (current_station)
client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client_socket.connect(sockfile);

while 1:
    station = current_station
    key = ReadKey()
    if power == 0: 
        if key == 2000: #power key
            player = PlayRadio (current_station)
            power = 1
            continue   
    elif power == 1:
        if key == 2000: #power key
            player.stdin.write("quit\n");
            power = 0;
            continue
        elif key == 1000: #chUP
            station = station - 1
        elif key == 1001: #chDOWN
            station = station + 1
        elif key == 1002: #volUP
            player.stdin.write("volume +47\n");
            continue
        elif key == 1003: #volDOWN
            player.stdin.write("volume -47\n");
            continue
        elif key == 1004: #mute
            player.stdin.write("mute\n");
            continue
        elif key == 1005: #play/pause
            player.stdin.write("pause\n");
            continue
        elif key == 1006: #set favor
            fd = open ('/root/NextRadio/favor.txt','w')
            fd.write(str(current_station))
            fd.close()
            favor = current_station
            continue
        elif key == 1007: #home, play favor
	    station = favor
        elif key >= 0 and key <= max_stations:
            station = key

        if station < 0:
            station = max_stations
        elif station > max_stations:
            station = 0
            
        if station >= 0 and station <= max_stations :
            current_station = station
            player = PlayRadio (current_station)
