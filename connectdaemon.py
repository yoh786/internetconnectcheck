import time
import urllib.request
import RPi.GPIO as GPIO
print("loaded. init vars and run")
# init
global keepgoing
global currtime
internet = True
timewait = 20
timeforrestart = 40
pin1 = 11
pin2 = 15
pin3 = 7
pin4 = 13
keepgoing = True
checkurl = 'http://google.com'
currtime = time.gmtime()


GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

GPIO.setup(pin1, GPIO.OUT)
GPIO.setup(pin2, GPIO.OUT)
print("prep switch")


som = input("START? (press enter)")
GPIO.output(pin1, False)
GPIO.output(pin2, False)

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
        GPIO.output(pin1, True)
        GPIO.output(pin2, True)
        time.sleep(10)
        GPIO.output(pin1, False)
        GPIO.output(pin2, False)
    except:
        print("failed GPIO")


def gpio_restart():
    try:
        gpio_pin_switch()
        time.sleep(timeforrestart)
        #below is check for internet again
        if check_internet():
            print("Restart success. Internet is UP")
            currtime = time.gmtime()
            print(time.asctime(currtime)) #there is a bug here - printing start time.
        else:
            keepgoing = False
            currtime = time.gmtime()
            print(time.asctime(currtime))
            GPIO.cleanup()
            holup = input("something is wrong...")

    except:
        print("catastrophic failure")
        GPIO.cleanup()
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
                print("DOWN\n.")
                gpio_restart()
                print("resume monitoring")
                time.sleep(t)
            
    except KeyboardInterrupt:
        GPIO.cleanup()

#program

print("starting loop")
main_loop(timewait)
print("closing GPIO")
GPIO.cleanup()
print("ending")
