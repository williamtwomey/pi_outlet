#!/usr/bin/python3

import os
import time
from threading import Thread

#hosts to ping
hosts = [ '8.8.8.8', '4.2.2.2', '1.2.3.4' ]


#number of fails before we activate relay
max_fail = 3

#percent of hosts that can be down before we consider it a failure
threshold = .3

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

while True:
        for i in hosts:
            t = Thread(target=ping, args=(i,))
            t.start()


	#ensure all threads have finished
        t.join()


        p = down / len(hosts)
        if p >= threshold:
            fail += 1

        down = 0

        print("percent failed: ", p)
        print("fails: ", fail)

        if fail == max_fail:
            print("max fails reached")
            #trigger relay, sleep for something crazy like 5min
            #os.system('gpio write 7 1') #else we get a brief power flicker before the actual reset
            #os.system('gpio mode 7 out')
            #os.system('gpio write 7 0')
            #Power off for 30 seconds
            #time.sleep(30)
            #os.system('gpio write 7 1') #turn it back on
            #time.sleep(300) #sleep for 5min to give it a chance
            fail = 0

	#wait 30s to run main loop again
        time.sleep(3)
