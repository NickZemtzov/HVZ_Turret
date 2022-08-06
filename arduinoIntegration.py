# arduinoIntegration.py
import serial
import time
import binascii

arduino = serial.Serial(port='/dev/cu.usbserial-14230', baudrate=115200, timeout=.1) # You must wait around 2 seconds after initializing before sending data or the handshake won't complete
def write_read(sent, expected):
    arduino.write(sent)
    data = bytes("", 'utf-8')
    while data != expected:
        data = arduino.readline()
    return data

while True:
    num = input("Enter ascii: ") # Taking input from user
    value = write_read(bytes(num,'utf-8'),bytes(str(ord(num)),'utf-8'))
    print(value) # printing the value




#TODO power the servos directly from the 5V not through the arduino becuase the current draw makes them worse

#NOTE for testing, plug in the 12V cuz it changes how much power the servos get which changes their operating parameters
