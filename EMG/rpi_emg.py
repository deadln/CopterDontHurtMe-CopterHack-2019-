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


class EMGTelemetryData:
    def __init__(self, emg1, emg2, trigger1, trigger2, accel1, accel2, pose1, pose2):
        """
        emg1,2: EMG data from both hands
        trigger1,2: if EMG data is higher than thresh
        accel1,2: accelerometer data from both hands
        pose1,2: recognized hand pose UP/DOWN/SIDE/NONE
        """
        self.emg1 = emg1
        self.emg2 = emg2
        self.trigger1 = trigger1
        self.trigger2 = trigger2
        self.accel1 = accel1
        self.accel2 = accel2
        self.pose1 = pose1
        self.pose2 = pose2

    def __str__(self):
        res = "EMG: {}, {}\nEMG Trigger: {}, {}\nAccelerometer: {}, {}\nPose: {}, {}"
        res = res.format(self.emg1, self.emg2, self.trigger1, self.trigger2, 
                         self.accel1, self.accel2, self.pose1, self.pose2)
        return res


class EMGTelemetry:
    """Class for reading data from Bitronics device"""
    def __init__(self, emg_thresh=10):
        """emg_thresh: trigger threshold for EMG sensors"""
        self.emg_thresh = emg_thresh
        self.ser = serial.Serial("/dev/serial0")
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()
        self.ser.baudrate = 38400

    def read(self):
        self.ser.write(b'A')
        time.sleep(0.005)

        data = self.ser.read(8)
        data = [float(ord(d)) for d in data]
        pulse1 = float(data[0] > 10.0)
        pulse2 = float(data[4] > 10.0)
        accel1 = np.array(data[1:4]) - 128.0
        accel2 = np.array(data[5:8]) - 128.0
        pose1 = accel1 / np.sqrt(np.sum(accel1**2))
        pose2 = accel2 / np.sqrt(np.sum(accel2**2))
        pose1 = get_direction(*pose1)
        pose2 = get_direction(*pose2)
        time.sleep(0.005)
        return EMGTelemetryData(data[0], data[4], pulse1, pulse2, 
                                accel1, accel2, pose1, pose2)       

if __name__=="__main__":
    telemetry = EMGTelemetry()
    while True:
        data = telemetry.read()
        print(data)
        print(" ")
        time.sleep(0.5)
    