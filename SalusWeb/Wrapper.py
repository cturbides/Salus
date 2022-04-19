"""Imports"""
from Wrapper_functions import *
import sys

"""GLobal Variables"""
BOARD = "Arduino UNO"
PORT = '/dev/ttyUSB0'
isBoard = True
dbAvailable = False
isSaving = False
preHeat = 3
roomId = sys.argv[1] if len(sys.argv) == 2 else None
counter_id = 1

WelcomeMessage(BOARD)
board = MakeConnection(PORT=PORT, BAUDRATE=9600)

"""Board is connected?"""
try:
    assert board != None
except: 
    isBoard = False
    
"""Database is available?"""
try:
    database = sqlite3.connect('db.sqlite3')
    cursor = database.cursor()
    dbAvailable = True
except:
    print(bcolors.FAIL + "[-] Database isn't available" + bcolors.ENDC)
    
while isBoard and dbAvailable:
    try:
        time.sleep(5) #Every 3 seconds we will save data inside the db
        if preHeat == 0:
            x = board.readline().decode('utf-8').split()
            x = WrappingData(x)
            SavingRoomData(
                           roomTemperature=x[0], 
                           patientTemperature=x[1],
                           roomHumidity=x[2],
                           roomDustLevel=x[3],
                           roomAirQuality=x[4],
                           patientPulse=x[5],
                           roomId=roomId,
                            db_cursor=cursor)
            database.commit() #Saving data inside the file
            print(bcolors.OKGREEN + "Data saved!" + bcolors.ENDC) if not isSaving else None
            isSaving = True
            if WhatsTheLastRowinRoom(cursor) == 20000:
                DeleteAllinRoom(cursor=cursor)
                print(bcolors.WARNING + "[-] Reseting Room table.." + bcolors.ENDC)
        else:
            preHeat -= 1
    except KeyboardInterrupt as keyboad:
        print(bcolors.FAIL + "\n[-] Keyboard interrupt, finishing program.." + bcolors.ENDC)
        DeleteAllinRoom(cursor)
        time.sleep(2)
        break
    except Exception as e:
        print(bcolors.WARNING + f"[-] Wrong data format!{e}" + bcolors.ENDC)
        time.sleep(1)

#If Board wasn't well connected       
if dbAvailable:
    database.commit() #Saving db
    cursor.close() #Closing db
print(bcolors.FAIL + "[-] Finishing connection!" + bcolors.ENDC)