from pad4pi import rpi_gpio
import time

# Setup Keypad

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

#keypad.cleanup()

def printKey(key):
  print(key)
  if (key=="1"):
    print("number")
  elif (key=="A"):
    print("letter")

# printKey will be called each time a keypad button is pressed
keypad.registerKeyPressHandler(printKey)

try:
  while(True):
    time.sleep(0.2)
except:
 keypad.cleanup()
