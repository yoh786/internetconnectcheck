#checks for internet
import urllib.request
import time


gox = True
x = True
intentionallyDuplicitiveVar = ''
currtime = ''

def check_internet():
    try:
        urllib.request.urlopen('http://google.com')
        return True
    except:
        return False

print('is the internet on?')

while gox == True:
    x = check_internet()
    currtime = time.gmtime()

    intentionallyDuplicitiveVar = str(x)

    print(x)
    print(time.asctime(currtime))
    with open('results.txt', 'a') as a_writer:
        a_writer.write(time.asctime(currtime) + '::') #notice the second part to convert to a string that you can print
        a_writer.write(intentionallyDuplicitiveVar)
        a_writer.write('\n--')

    time.sleep(180)
