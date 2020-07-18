import GT_521F52
import time

try:
    p = GT_521F52.PyFingerprint_GT_521F52('/dev/ttyUSB0')

except Exception as e:
    print("Something went wrong")
    print('Exception message: ' + str(e))


try:

    p.delete_all()
except Exception as e:
    print('Exception message: ' + str(e))
