#!/usr/bin/python3

import os
import time
from threading import Thread

hosts = [ '8.8.8.8', '4.2.2.2', '8.8.8.91' ]
trigger = "False"

def ping(i):
    code = os.system('ping -c 3 ' + i + ' >/dev/null')
    print("thread exited with code ", code)
    if code > 0:
        global trigger
        trigger = "True"


for i in hosts:
    t = Thread(target=ping, args=(i,))
    t.start()
    t.join()

print("main script")
print("trigger: ", trigger)
