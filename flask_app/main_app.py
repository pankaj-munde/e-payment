from pad4pi import rpi_gpio
import time
import sys
import serial
import sqlite3
from sqlite3 import Error

# fair per km
km_rate = 2
# options Srings
location_data = [{"loc_0":"Pune", "dist_0":0},
                 {"loc_1":"Shivajinagar", "dist_1":5},
                 {"loc_2":"Dapodi", "dist_2":15},
                 {"loc_3":"Pimpri", "dist_3":25},
                 {"loc_4":"Chinchwad", "dist_4":30},
                 {"loc_5":"Akurdi", "dist_5":40}
                ]
# database name
database = r"user_database.db"

# Setup Keypad
start_point = ''
end_point = ''
key_cnt = 1

KEYPAD = [
        ["D","C","B","A"],
        ["#","9","6","3"],
        ["0","8","5","2"],
        ["*","7","4","1"]
]

# same as calling: factory.create_4_by_4_keypad, still we put here fyi:
ROW_PINS = [0, 5, 6, 13] # BCM numbering
COL_PINS = [19, 26, 20, 21] # BCM numbering

factory = rpi_gpio.KeypadFactory()

# Try factory.create_4_by_3_keypad
# and factory.create_4_by_4_keypad for reasonable defaults

keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)


## Supporting Functions

def cleanup():
  global keypad
  keypad.cleanup()

def get_point(key):
  global key_cnt
  global start_point
  global end_point
  #key_cnt += 1
  

  if key_cnt == 1:
    start_point = key
    sys.stdout.write("\033[F")
    print('[Info]| Select Destination of journey: ', start_point)
    print('[Info]| Select Destination of journey: ')
    
  if key_cnt == 2:
    end_point = key
    sys.stdout.write("\033[F")
    print('[Info]| Select Destination of journey: ', end_point)
  key_cnt += 1

def key_scan():
    
  try:
      
      keypad.registerKeyPressHandler(get_point)
      pr_flag = True
      while True:
        if pr_flag:
          pr_flag = False
        time.sleep(1)
        if key_cnt > 2:
          break
        
  except KeyboardInterrupt:
      print("Goodbye")
  finally:
      cleanup()

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        # print("DB Connection Established Successfully")
        return conn
    except Error as e:
        print(e)

    return conn

def match_fingerprint():
    import GT_521F52

    try:
        p = GT_521F52.PyFingerprint_GT_521F52('/dev/ttyUSB0')

    except Exception as e:
        print("Something went wrong")
        print('Exception message: ' + str(e))

    try:
        print('[Info]| Put your inger on scanner')
        fid = p.IdentifyUser()
        p.off_Led()
        
        if fid:
            print('[Info]| User identifiaction successful with id : {}'.format(fid))
            _print_br(63)
            return fid
        else:
            print('[Info]| User identifiaction failed')
            _print_br(63)
            match_fingerprint()
    except Exception as e:
        # print('Exception message: ' + str(e))
        pass

def _print_br(n):
    for i in range(n):
        print("_", end='_')
    print('\n')

def _get_dist(point):
    point = int(point) - 1
    return location_data[int(point)]['dist_'+str(point)]

def _dist_calc(start_point, end_point):
    return end_point - start_point

def get_bal(fid):
    """Fetch available balance information of user"""
    time.sleep(0.1)
    con = create_connection(database)
    con = create_connection("user_database.db")
    cur = con.cursor()
    sql_qry = """SELECT * FROM user_info where fid = ?"""
    cur.execute(sql_qry, (str(fid),))
    users = cur.fetchall()
    con.close()
    return  users[0][-2]

def get_mnum(fid):
    time.sleep(0.1)
    con = create_connection(database)
    con = create_connection("user_database.db")
    cur = con.cursor()
    sql_qry = """SELECT * FROM user_info where fid = ?"""
    cur.execute(sql_qry, (str(fid),))
    users = cur.fetchall()
    con.close()
    return  users[0][-3]

def update_bal(fid, bal):
    """Update balance in database"""
    time.sleep(0.1)
    con = create_connection('user_database.db')
    cursor = con.cursor()
    sql_update_query = """Update user_info set bal = ? where fid = ?"""
    data = (str(bal), str(fid))
    cursor.execute(sql_update_query, data)
    con.commit()
    print("[Info]| Record Updated successfully")
    _print_br(63)
    cursor.close()

def show_locs():
    """Print out Journey points"""

    _print_br(63)
    print('[info]| Following Stops Will be includes in journey: ')
    _print_br(63)
    for idx,locs in enumerate(location_data):
        print("{}. {}".format(idx+1, locs['loc_'+str(idx)]))    
    _print_br(63)
    print('[Info]| Select Source of journey: ')

def show_dist():
    """ Shows starting options"""
    _print_br(63)
    total_dist = _dist_calc(_get_dist(start_point), _get_dist(end_point))
    print("[info]| Total Distance of your Journey : {} km".format(total_dist))
    _print_br(63)
    return total_dist

def show_price(total_dist):
    total_fair = total_dist*km_rate
    print("Total fair is: {} ruppees".format(total_fair))
    _print_br(63)
    return total_fair

def send_sms(total_fair, fid):
    phone = serial.Serial("/dev/ttyAMA0",  11500, timeout=5)
    mobile_no = get_mnum(fid)
    message = "Your account is debited for INR {}.\nAvailable balance is INR {}.\nThank you for travelling with us.\nHappy Journey".format(total_fair, get_bal(fid))
    try:

        time.sleep(0.5)
        phone.write(b'ATZ\r')
        time.sleep(0.5)
        phone.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        phone.write(b'AT+CMGS="' + mobile_no.encode() + b'"\r')
        time.sleep(0.5)
        phone.write(message.encode() + b"\r")
        time.sleep(0.5)
        phone.write(bytes([26]))
        time.sleep(0.5)
    finally:
        phone.close()


if __name__ == "__main__":
    
    # Show Journey Points
    show_locs()

    key_scan()
    # Show Dist calculation
    total_dist = show_dist()

    # Show Journey Price
    total_fair = show_price(total_dist)
    # Get fingerprint matched
    fid = match_fingerprint()
    if fid:
        # Get user balance from database
        bal = get_bal(fid)
        update_bal(fid, bal-total_fair)
        #print('[Info]| Available balance is {}'.format(get_bal(fid)))
        send_sms(total_fair, fid)
    else:
        print('[Info]| Please check fingerprint scanner is connected properly.')
        _print_br(63)

