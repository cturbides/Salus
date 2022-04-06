from typing import List
import serial
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def WelcomeMessage(BOARD:str) -> None:
    print(bcolors.BOLD + bcolors.HEADER + "Serial Wrapper" + bcolors.ENDC)
    print(bcolors.OKGREEN + "Board: " + BOARD + bcolors.ENDC + "\n"+
    bcolors.OKGREEN + "Sensors: DHT22, MQ-2, MQ-135, Dust Sensor" + bcolors.ENDC + "\n" +
    bcolors.WARNING + "[+] Trying to connect " + BOARD + "..." + bcolors.ENDC)
    
def MakeConnection(PORT: str, BAUDRATE:int) -> serial.Serial:
    for i in range(5):
        try:
            board = serial.Serial(PORT, baudrate=BAUDRATE)
            print(bcolors.OKGREEN + "[+] Connection established!" + bcolors.ENDC)
            time.sleep(2)
            return board
        except:
            print(bcolors.FAIL + '[-] Failed trying to connect Arduino board by Serial' + bcolors.ENDC)
            print(bcolors.WARNING + '--->Trying again..' + bcolors.ENDC)
            time.sleep(2)
    return None

def WrappingData(decodedString:str) -> List:
    return 