import time
from Wrapper_functions import *

BOARD = "Arduino UNO"
PORT = '/dev/ttyACM0'
isBoard = True

WelcomeMessage(BOARD)
board = MakeConnection(PORT=PORT, BAUDRATE=9600)

try:
    assert board != None
except: 
    isBoard = False
    
while isBoard:
    try:
        x = board.readline().decode('utf-8').split()
        WrappingData(x)
    except:
        print(bcolors.WARNING + "[-] Wrong data format!" + bcolors.ENDC)
        time.sleep(1)
#If Board wasn't well connected       
print(bcolors.FAIL + "[-] Failed connection!" + bcolors.ENDC)