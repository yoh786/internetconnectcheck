#checks for internet
import urllib.request
import time

x = True

def check_internet():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

while x == True:
    x = check_internet()
    print(x)
    time.sleep(60)
