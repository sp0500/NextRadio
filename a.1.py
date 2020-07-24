#############################################
# 
# Python script for NextRadio (a.py) 
# Version: 1.0
#
# Created by Aladdin
#
# Changes Logs:
# [2013-04-20] By A-Lang
#              Replaced the lircrc with the mplayer's subordinate mode
#              Added the audio volume control
#              Added the Mute,Power keys function
#

import socket
import re
import os 
import subprocess
from subprocess import Popen, PIPE

i = 0
stationlist=[]
funkey = 0
power = 1
max_stations = 0
current_station = 0
sockfile = '/dev/lircd'

def PlayRadio(station):
   global player

   if (power == 1):
       os.system("killall " + "mplayer");
       current_station = station
       print current_station
       Play_station = "mplayer -ao oss -subordinate -quiet -cache 256 " + stationlist[current_station].rstrip("\n") + " < /dev/null &"
       player = subprocess.Popen(Play_station.split(" "), stdin=PIPE)

fd = open ("/root/NextRadio/radio.pls","r")
for line in fd:
    msg = re.search('^#',line)
    if msg:
       print "."
    else:
       stationlist.append(line)
       i = i+1

fd.close()

max_stations = i-1
print stationlist[max_stations]
PlayRadio (current_station)
client_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client_socket.connect(sockfile);


def ProcessKey(current_station):
    station_num = 0
    funckey = 0
    while 1:
        data = client_socket.recv(512)
        cmd_list = data.split( " " )
        if (cmd_list[1] == "00"):
            if (cmd_list[2][0] == 'D'):
                station_number = funckey + int (cmd_list[2][1])
                funckey = 0
                return station_number
            elif (cmd_list[2][0] == 'R'):
                funckey = funckey + 10
            elif (cmd_list[2][0] == 'G'):
                funckey = funckey + 20
            elif (cmd_list[2][0] == 'Y'):
                funckey = funckey + 30
            elif (cmd_list[2][0] == 'B'):
                funckey = funckey + 40

            elif (cmd_list[2] == "chUp" or cmd_list[2] == "chUp_V2"):
                return current_station - 1

            elif (cmd_list[2] == "chDown" or cmd_list[2] == "chDown_V2"):
                return current_station + 1

            elif (cmd_list[2] == "volUp" or cmd_list[2] == "volUp_V2"):
                player.stdin.write("volume +47\n")

            elif (cmd_list[2] == "volDown" or cmd_list[2] == "volDown_V2"):
                player.stdin.write("volume -47\n")

            elif (cmd_list[2] == "power"):
                funckey = 0
                return 1200
         
            elif (cmd_list[2] == "mute"):
                player.stdin.write("mute\n")
                

while 1:
    station = ProcessKey(current_station)
    if (station < -1):
        continue
    elif (station == 1200):
        if (power == 1):
            power = 0
            player.stdin.write("quit\n")
        else:
            power = 1
            PlayRadio(current_station)
        continue
    elif (station == current_station):
        continue
    elif (station > max_stations + 1):
        continue
    elif (station == max_stations + 1):
        station = 0;
    elif (station == -1):
        station = max_stations
    if power == 1 and station >= 0 and station <= max_stations :
        current_station = station
        PlayRadio (station)
