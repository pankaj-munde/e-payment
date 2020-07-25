from pad4pi import rpi_gpio
import time

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
    print('[Info]| Select Source of journey: ', start_point)
      
  if key_cnt == 2:
    end_point = key
    print('[info]| Select Destination of journey: ', end_point)
  key_cnt += 1


try:
 
    keypad.registerKeyPressHandler(get_point)
   
    while True:
        time.sleep(1)
        if key_cnt > 2:
          break
        
except KeyboardInterrupt:
    print("Goodbye")
finally:
    cleanup()
