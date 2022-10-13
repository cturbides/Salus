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

def welcome_message(BOARD:str) -> None:
    print(bcolors.BOLD + bcolors.HEADER + "Serial Wrapper" + bcolors.ENDC)
    print(
        bcolors.OKGREEN + "Board: " + BOARD + bcolors.ENDC + "\n" +
        bcolors.OKGREEN + "Sensors: DHT22, MQ-2, MQ-135, Dust Sensor" + bcolors.ENDC + "\n" +
        bcolors.WARNING + "[+] Trying to connect " + BOARD + "..." + bcolors.ENDC
    )
    
def make_connection(PORT: str, BAUDRATE:int) -> serial.Serial:
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

def wrapping_data(string_decoded:list) -> List:
    try:
        for i in range(len(string_decoded)):
            assert type(string_decoded[i]) == str
    except:
        return []
    
    """
    roomTemperature = string_decoded[0]
    patientTemperature = string_decoded[1]
    roomHumidity = string_decoded[2]
    roomDustLevel = string_decoded[3]
    roomAirQuality = string_decoded[4]
    patientPulse = string_decoded[5]
    patientElectro = string_decoded[6]
     """

    return [string_decoded[0], string_decoded[1],
            string_decoded[2], string_decoded[3],
            string_decoded[4], string_decoded[5],
            string_decoded[6]]

def saving_room_data(
               room_temperature: str,
               patient_temperature: str,
               room_humidity: str,
               room_dust_level: str,
               room_air_quality: str,
               patient_pulse: str,
               patient_electro: str,
               room_id: str,
               db_cursor: sqlite3.Cursor) -> None:
    
    """
    Data without format and well converted!
    """
    room_temperature = float(room_temperature) if len(room_temperature) != 0 else None
    patient_temperature = float(patient_temperature) if len(patient_temperature) != 0 else None
    room_humidity = float(room_humidity) if len(room_humidity) != 0 else None
    room_dust_level = float(room_dust_level) if len(room_dust_level) != 0 else None
    room_air_quality = float(room_air_quality) if len(room_air_quality) != 0 else None
    patient_pulse = float(patient_pulse) if len(patient_pulse) != 0 else None
    patient_electro = float(patient_electro) if len(patient_electro) != 0 else None
    
    """
    Trying to save the data!
    """
    if not None in {room_temperature, patient_temperature, room_humidity, room_dust_level,
                    room_air_quality, patient_pulse, patient_electro}:
        
        db_cursor.execute(
        """
        INSERT INTO salusApp_sensores ( roomTemperature, patientTemperature, 
                                        roomHumidity, roomDustLevel, roomAirQuality,
                                        patientPulse, patientElectro, room_id)
        VALUES (?,?,?,?,?,?,?,?);
        """,
        (room_temperature, patient_temperature, room_humidity, \
        room_dust_level,room_air_quality, patient_pulse, patient_electro, room_id))
    
    else:
        print(bcolors.WARNING + "[-] There's a value missing!" + bcolors.ENDC)

def whats_in_the_last_row_of_room(cursor: sqlite3.Cursor) -> int:
    cursor.execute(
    """
    SELECT id FROM salusApp_sensores ORDER BY id DESC LIMIT 1;
    """)
    id = int(cursor.fetchone()[0])
    return id

def delete_all_in_room(cursor: sqlite3.Cursor) -> None:
    cursor.execute(
    """
    DELETE FROM salusApp_sensores WHERE id < 20001;
    """)
    cursor.execute(
    """
    UPDATE sqlite_sequence SET seq=0 WHERE name = 'salusApp_sensores';
    """)
