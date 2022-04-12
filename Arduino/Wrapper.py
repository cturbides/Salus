"""Imports"""
from Wrapper_functions import *

"""GLobal Variables"""
BOARD = "Arduino UNO"
PORT = '/dev/ttyUSB0'
isBoard = True
dbAvailable = False
isSaving = False
preHeat = 3

WelcomeMessage(BOARD)
board = MakeConnection(PORT=PORT, BAUDRATE=9600)

"""Board is connected?"""
try:
    assert board != None
except: 
    isBoard = False

"""Database is available?"""
try:
    database = sqlite3.connect('datawrapped.db')
    cursor = database.cursor()
    dbAvailable = True
except:
    print(bcolors.FAIL + "[-] Database isn't available" + bcolors.ENDC)

while isBoard and dbAvailable:
    try:
        time.sleep(3) #Every 3 seconds we will save data inside the db
        if preHeat == 0:
            x = board.readline().decode('utf-8').split()
            x = WrappingData(x)
            SavingRoomData(DHT22=x[0], 
                            MQ2=x[1],
                            MQ135=x[2],
                            DustSensor=x[3],
                            db_cursor=cursor)
            database.commit() #Saving data inside the file
            print(bcolors.OKGREEN + "Data saved!" + bcolors.ENDC) if not isSaving else None
            isSaving = True
            if WhatsTheLastRowinRoom(cursor) == 20000:
                DeleteAllinRoom()
                print(bcolors.WARNING + "[-] Reseting Room table.." + bcolors.ENDC)
        else:
            preHeat -= 1
    except KeyboardInterrupt as keyboad:
        print(bcolors.FAIL + "\n[-] Keyboard interrupt, finishing program.." + bcolors.ENDC)
        time.sleep(2)
        break
    except:
        print(bcolors.WARNING + "[-] Wrong data format!" + bcolors.ENDC)
        time.sleep(1)

#If Board wasn't well connected       
if dbAvailable:
    database.commit() #Saving db
    cursor.close() #Closing db
print(bcolors.FAIL + "[-] Finishing connection!" + bcolors.ENDC)