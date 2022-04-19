"""Imports"""
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
    for _ in range(5):
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
            decodedString[2], decodedString[3],
            decodedString[4], decodedString[5]]

def SavingRoomData(
               roomTemperature: str,
               patientTemperature: str,
               roomHumidity: str,
               roomDustLevel: str,
               roomAirQuality: str,
               patientPulse: str,
               roomId: str,
               db_cursor: sqlite3.Cursor) -> None:
    
    """
    Data without format and well converted!
    """
    roomTemperature = float(roomTemperature) if len(roomTemperature) != 0 else None
    patientTemperature = float(patientTemperature) if len(patientTemperature) != 0 else None
    roomHumidity = float(roomHumidity) if len(roomHumidity) != 0 else None
    roomDustLevel = float(roomDustLevel) if len(roomDustLevel) != 0 else None
    roomAirQuality = float(roomAirQuality) if len(roomAirQuality) != 0 else None
    patientPulse = float(patientPulse) if len(patientPulse) != 0 else None
    
    """
    Trying to save the data!
    """
    if roomTemperature != None and patientTemperature != None and \
        roomHumidity != None and roomDustLevel != None and \
            roomAirQuality != None and patientPulse != None:
        db_cursor.execute("""
        INSERT INTO salusApp_sensores ( roomTemperature, patientTemperature, 
                                        roomHumidity, roomDustLevel, roomAirQuality,
                                        patientPulse, room_id)
        VALUES (?,?,?,?,?,?,?);
                            """,
        (roomTemperature, patientTemperature, roomHumidity, roomDustLevel,roomAirQuality, patientPulse, roomId))
    else:
        print(bcolors.WARNING + "[-] There's a value missing!" + bcolors.ENDC)

def WhatsTheLastRowinRoom(cursor: sqlite3.Cursor) -> int:
    cursor.execute("""
    SELECT id FROM salusApp_sensores ORDER BY id DESC LIMIT 1
                   """)
    id = int(cursor.fetchone()[0])
    return id

def DeleteAllinRoom(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
    DELETE FROM salusApp_sensores WHERE id < 20001;
                       """)
    cursor.execute("""
                   UPDATE sqlite_sequence SET seq=0 WHERE name = 'salusApp_sensores';
                   """)