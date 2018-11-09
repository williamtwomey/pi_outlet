#!/usr/bin/python3

import os
import time
from threading import Thread

hosts = [ '8.8.8.8', '4.2.2.2', '1.2.3.4' ]
trigger = "False"
max_fail = 3
fail = 0
GPIO = 7

def ping(i):
    code = os.system('ping -c 3 ' + i + ' >/dev/null')
    print("thread exited with code ", code)
    if code > 0:
        global trigger
        trigger = "True"


while True:
        for i in hosts:
            t = Thread(target=ping, args=(i,))
            t.start()


	#ensure all threads have finished
        t.join()

        print("main script")
	
        if trigger == "True":
            fail += 1
            trigger = "False"

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
