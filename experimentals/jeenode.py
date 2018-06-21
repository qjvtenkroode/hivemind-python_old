import serial
import sys

s = serial.Serial('/dev/cu.usbserial-AI03DA56', 57600)
while True:
    line = s.readline()
    print(line)
