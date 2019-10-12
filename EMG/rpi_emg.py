#Sending the data thorugh UART 
#UART PINOUT
#Rx -> GPIO15
#Tx -> GPIO14

# get the GPIO Library
import RPi.GPIO as GPIO
import serial
import numpy as np
import time

def get_direction(x, y, z):
    if x < -0.9:
        return 'UP'
    elif x > 0.9:
        return 'DOWN'
    elif x < 0.1:
        return 'SIDE'
    else:
        return 'NONE'

def main():
    #Open named port 
    ser = serial.Serial ("/dev/serial0")

    #Setting up the GPIO Pins
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    ser.baudrate = 38400

    while True:
        ser.write(b'A')
        time.sleep(0.005)

        data = ser.read(8)
        data = [float(ord(d)) for d in data]
        pulse1 = float(data[0] > 10.0)
        pulse2 = float(data[4] > 10.0)
        accel1 = np.array(data[1:4]) - 128.0
        accel1 /= np.sqrt(np.sum(accel1**2))
        accel2 = np.array(data[5:8]) - 128.0
        accel2 /= np.sqrt(np.sum(accel2**2))
        pose1 = get_direction(*accel1)
        pose2 = get_direction(*accel2)
        print(pulse1, pulse2, pose1, pose2)
        time.sleep(0.080)
        
    ser.close()        

if __name__=="__main__":
    main()
else:
    print('Oops')

#End of the Script