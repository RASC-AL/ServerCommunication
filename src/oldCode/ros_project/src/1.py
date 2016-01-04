import ros.py
import serial
arduino=serial.Serial('/dev/ttyACM0', 9600)
arduino.write('0,0,0,0,0')

