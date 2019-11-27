import serial
import time

ser = serial.Serial('/dev/ttyS0', 115200, timeout=1)
ser.close()
ser.open()

while True:
    if ser.inWaiting():
        entry = ser.readline()
        print(entry.decode('utf-8'))
