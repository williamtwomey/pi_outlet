#!/usr/bin/python3

import os
import time
from threading import Thread

#How often we should ping (s)
LOOP_TIME = "10"

#number of fails before we activate relay
MAX_FAIL = 3

# LOOP_TIME * MAX_FAIL = Time to detect failure and trigger relay

#hosts to ping
hosts = [ '8.8.8.8', '4.2.2.2', '1.1.1.1' ]

#host local to us that should always be up (generally default gateway)
#otherwise just use localhost (127.0.0.1)
monitor = "127.0.0.1"

#percent of hosts that can be down before we consider it a failure
#1=100%, .5=50%, etc.
threshold = 1

fail = 0
down = 0

#GPIO pin
GPIO = 7

def ping(i):
    code = os.system('ping -c 3 ' + i + ' >/dev/null')
    print(i," ", code)
    if code > 0:
        global down
        down += 1

#Main loop
while True:
        #ensure our monitor IP is up, otherwise no point in continuing
        if os.system('ping -c 3 ' + monitor + ' >/dev/null') > 0:
            #Our monitor IP is down, so we should do nothing
            print("monitor ip ", monitor, " is down")
            time.sleep(1)
        else:
            #start ping threads
            for i in hosts:
                t = Thread(target=ping, args=(i,))
                t.start()
            #ensure all threads have finished
            t.join()

            #determine % of failed hosts
            p = down / len(hosts)
            if p >= threshold:
                fail += 1

            down = 0

            print("percent failed: ", p)
            print("fails: ", fail)

            if fail == MAX_FAIL:
                print("max fails reached")
                #os.system('gpio write 7 1') #else we get a brief power flicker when changing the mode
                #os.system('gpio mode 7 out')
                #os.system('gpio write 7 0')
                #Power off for 30 seconds
                #time.sleep(30)
                #os.system('gpio write 7 1') #turn it back on
                #time.sleep(300) #sleep for 5min to give it a chance
                fail = 0
     
            #wait 30s to run main loop again
            time.sleep(int(LOOP_TIME))
