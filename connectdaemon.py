import time
import urllib.request
import RPi.GPIO as GPIO
print("loaded. init vars and run")
# init
global keepgoing
global currtime
internet = True
timewait = 60
timeforrestart = 300
pin1 = 3
pin2 = 5
keepgoing = True
checkurl = 'http://google.com'
currtime = time.gmtime()

#INIT GPIO section

som = input("START? (press enter)")

# Functions
def check_internet():
    try:
        urllib.request.urlopen(checkurl)
        return True
    except:
        return False

def gpio_pin_switch():
    try:
        GPIO.setmode(GPIO.BOARD)
        print("Restarting router")
        GPIO.setup(3, GPIO.OUT)
        GPIO.setup(5, GPIO.OUT)
        time.sleep(5)

        GPIO.cleanup()

    except:
        print("failed GPIO")

def gpio_cleanup():
    GPIO.cleanup()
    print("cleanup")

def gpio_restart():
    try:
        gpio_pin_switch()
        time.sleep(timeforrestart)
        #below is check for internet again
        if check_internet():
            print("Restart success. Internet is UP")
            currtime = time.gmtime()
            print(time.asctime(currtime))
        else:
            keepgoing = False
            currtime = time.gmtime()
            print(time.asctime(currtime))
            gpio_cleanup()
            holup = input("something is wrong...")

    except:
        print("catastrophic failure")
        gpio_cleanup()
        holup = input("something is wrong...")


def main_loop(t):
    try:
        while keepgoing:
            currtime = time.gmtime()
            print(time.asctime(currtime))
            internet = check_internet()

            if internet:
                print("UP\n.")
                time.sleep(t)
            else:
                print('possibly down.. checking..')
                doublecheck = False
                time.sleep(40)
                doublecheck = check_internet()
#you might want to change below so the default safe option is actually to keep it on, for the ELSE
                if doublecheck:
                    print('possible false alarm')
                else:
                    print("DOWN\n.")
                    gpio_restart()

                print("resume monitoring")
                time.sleep(t)

    except KeyboardInterrupt:
        gpio_cleanup()

#program

print("starting loop")
main_loop(timewait)
print("closing GPIO")
GPIO.cleanup()
print("ending")
