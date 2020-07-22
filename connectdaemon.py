import time
import urllib.request
#import RPi.GPIO as gpio
print("loaded. init vars and run")
# init
global keepgoing
internet = True
timewait = 10
timeforrestart = 30
pin1 = 1
pin2 = 2
pin3 = 3
pin4 = 4
keepgoing = True
switch = ''
checkurl = 'http://google.com'
currtime = time.gmtime()


# Functions
def check_internet():
    try:
        urllib.request.urlopen(checkurl)
        return True
    except:
        return False

def gpio_pin_switch():
    try:
        print("Restarting router")
    except:
        print("failed GPIO")

def gpio_restart():
    try:
        gpio_pin_switch()
        time.sleep(timeforrestart)
        #below is check for internet again
        if check_internet():
            print("Restart success. Internet is UP")
            print(time.asctime(currtime))
        else:
            keepgoing = False
            print(time.asctime(currtime))
            holup = input("something is wrong...")
    except:
        print("catastrophic failure")
        holup = input("something is wrong...")


def main_loop(t):
    while keepgoing:
        currtime = time.gmtime()
        print(time.asctime(currtime))
        internet = check_internet()

        if internet:
            print("UP\n.")
            time.sleep(t)
        else:
            print("DOWN\n.")
            gpio_restart()
            print("resume monitoring")
            time.sleep(t)


#program

print("starting loop")
main_loop(timewait)
print("ending")
