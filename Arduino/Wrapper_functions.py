"""Imports"""
from lib2to3.pgen2.token import MINEQUAL
from typing import List
import serial
import time
import sqlite3

"""Colors font on terminal"""
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

def WrappingData(decodedString:list) -> List:
    try:
        for i in range(len(decodedString)):
            assert type(decodedString[i]) == str
    except:
        return []
    
    """
    Room:
        dht22 = decodedString[0]
        wq_2 = decodedString[1]
        wq_135 = decodedString[2]
        dust_sensor = decodedString[3]
    Paciente:
    """
    return [decodedString[0], decodedString[1],
            decodedString[2], decodedString[3]]

def SavingRoomData(DHT22: str,
               MQ2: str,
               MQ135: str,
               DustSensor: str,
               db_cursor: sqlite3.Cursor) -> None:
    DHT22 = float(DHT22) if len(DHT22) != 0 else None
    MQ2 = float(MQ2) if len(MQ2) != 0 else None
    MQ135 = float(MQ135) if len(MQ135) != 0 else None
    DustSensor = float(DustSensor) if len(DustSensor) != 0 else None
    if DHT22 != None and MQ2 != None and \
        MQ135 != None and DustSensor != None:
        db_cursor.execute("""
        INSERT INTO Room (DHT22, MQ2, MQ135, DustSensor)
        VALUES (?,?,?,?);
                            """,(DHT22, MQ2, MQ135, DustSensor))
def WhatsTheLastRowinRoom(cursor: sqlite3.Cursor) -> int:
    cursor.execute("""
    SELECT id FROM Room ORDER BY id DESC LIMIT 1
                   """)
    id = int(cursor.fetchone()[0])
    return id
def DeleteAllinRoom(cursor: sqlite3.Cursor) -> None:
    cursor.executemany("""
    DELETE FROM Room WHERE id < 20001;
    UPDATE sqlite_sequence SET seq=0 WHERE name = 'Room';
                       """)