"""Imports"""
from wrapper_functions.py import *
import sys

"""GLobal Variables"""
BOARD = "Arduino MEGA"
PORT = '/dev/ttyACM0'
is_board = True
db_is_available = False
is_saving = False
heating = 3
room_id = sys.argv[1] if len(sys.argv) == 2 else None
counter_id = 1  # Room id

"""MAKING THE CONNECTION"""
welcome_message(BOARD)
board = make_connection(PORT=PORT, BAUDRATE=9600)

"""Is Board connected?"""
try:
    assert board != None
except:
    is_board = False

"""Is Database available?"""
try:
    database = sqlite3.connect('./SalusWeb/db.sqlite3')
    cursor = database.cursor()
    db_is_available = True
except:
    print(bcolors.FAIL + "[-] Database isn't available" + bcolors.ENDC)

"""If board and db available?"""
while is_board and db_is_available:
    try:
        time.sleep(1)  # Every second we'll save data inside the db
        if not heating:
            x = board.readline().decode('utf-8').split()
            x = wrapping_data(x)
            saving_room_data(
                room_temperature=x[0],
                patient_temperature=x[1],
                room_humidity=x[2],
                room_dust_level=x[3],
                room_air_quality=x[4],
                patient_pulse=x[5],
                patient_electro=x[6],
                room_id=room_id,
                db_cursor=cursor)
            database.commit()  # Saving the file
            print(bcolors.OKGREEN + "Data saved!" +
                  bcolors.ENDC) if not is_saving else None
            is_saving = True
            if whats_in_the_last_row_of_room(cursor) == 20000:
                delete_all_in_room(cursor=cursor)
                print(bcolors.WARNING +
                      "[-] Reseting Room table.." + bcolors.ENDC)
        else:
            heating -= 1

    except KeyboardInterrupt as keyboad:
        print(bcolors.FAIL +
              "\n[-] Keyboard interrupt, finishing program.." + bcolors.ENDC)
        time.sleep(2)
        break
    except EOFError as ctrlz:
        print(bcolors.FAIL +
              "\n[-] Keyboard interrupt, finishing program.." + bcolors.ENDC)
        delete_all_in_room(cursor)
        time.sleep(2)
        break
    except Exception as e:
        print(bcolors.WARNING + f"[-] Wrong data format! {e}" + bcolors.ENDC)
        time.sleep(1)

"""If we were connected to the db"""
if db_is_available:
    database.commit()  # Saving db
    cursor.close()  # Closing db
print(bcolors.FAIL + "[-] Finishing connection!" + bcolors.ENDC)
