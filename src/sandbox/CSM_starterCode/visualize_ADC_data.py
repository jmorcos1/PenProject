import math
import time
import board
import busio
import threading
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode
import struct

# Data collection setup
RATE = 860
SAMPLES = 50
# Create the I2C bus with a fast frequency
# NOTE: Your device may not respect the frequency setting
#       Raspberry Pis must change this in /boot/config.txt
#i2c = busio.I2C(board.SCL, board.SDA)
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
#this was set on pi
#https://www.raspberrypi-spy.co.uk/2018/02/change-raspberry-pi-i2c-bus-speed/
# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
#single-ended input
chan0 = AnalogIn(ads, ADS.P0)
#Configure ADC
ads.mode = Mode.CONTINUOUS
ads.data_rate = RATE
sample_interval = 1.0 / ads.data_rate
# First ADC channel read in continuous mode configures device
# and waits 2 conversion cycles
_ = chan0.value


def sampleADC():
    repeats = 0
    skips = 0
    #data = [None] * SAMPLES
    data = np.array(([0] * SAMPLES), dtype="int16")
    start = time.monotonic()
    time_next_sample = start + sample_interval
    # Read the same channel over and over
    for i in range(SAMPLES):
        # Wait for expected conversion finish time
        while time.monotonic() < (time_next_sample):
            pass
        # Read conversion value for ADC channel
        #data[i] = np.uint16(val.to_bytes(2, "big", signed=False))
        #data[i] = np.uint16(struct.unpack(">h", val.to_bytes(2, "big", signed=False))[0]) 
        #data[i] = val.to_bytes(2, "big", signed=False)
        data[i] = chan0.value
        #if (data[i] > 62000) or (data[i] < 1):
         #   data[i] = 1
        if data[i] < 1:
            data[i] = 1
        # Loop timing
        time_last_sample = time.monotonic()
        time_next_sample = time_next_sample + sample_interval
        if time_last_sample > (time_next_sample + sample_interval):
            skips += 1
            time_next_sample = time.monotonic() + sample_interval
        # Detect repeated values due to over polling
        if data[i] == data[i - 1]:
            repeats += 1
    end = time.monotonic()
    total_time = end - start
    #print(total_time)
    #return np.mean(data, dtype="uint16")
    #return np.int16(math.floor(np.int16(sum(data)/len(data))))
    #return np.int16(math.floor(sum(data)/len(data)))
    return math.floor(sum(data)/len(data))

nFactors = 14
sFactor = 0.3
minThresh = 3.75
expectedRange = 0.18
maxThresh = minThresh + expectedRange 
factorScale = np.array([sFactor])

while len(factorScale) < nFactors:
    sFactor *= 1.14
    factorScale = np.append(factorScale, sFactor)

print(factorScale)

thresholdScale = dict(zip(np.around(np.linspace(minThresh, 3.88, 14), 3), np.around(factorScale, 2)))

print(thresholdScale)


def getFactor(val, threshDict):
    for thr in reversed(list(threshDict.keys())):
        if val > float(thr):
            return threshDict[thr]
    return 0





class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        
    def callback(self):
        self.root.quit()

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)
        self.root.title('Analog Voltage')
        self.root.geometry("400x200")
        
        self.s1 = tk.StringVar()
        self.s2 = tk.StringVar()
        self.s3 = tk.StringVar()
        self.s4 = tk.StringVar()
        self.s5 = tk.StringVar()
        self.s6 = tk.StringVar()
        
        self.s1.set('   V_Dig     |')
        self.s2.set('   log_10(V_Dig)   |')
        self.s3.set('   lw Scale Factor')
        #self.s4.set('1')
        #self.s5.set('0')
        #self.s6.set('0')
        
        myLabel1 = tk.Label(self.root, textvariable = self.s1)
        myLabel2 = tk.Label(self.root, textvariable = self.s2)
        myLabel3 = tk.Label(self.root, textvariable = self.s3)
        myLabel4 = tk.Label(self.root, textvariable = self.s4)
        myLabel5 = tk.Label(self.root, textvariable = self.s5)
        myLabel6 = tk.Label(self.root, textvariable = self.s6)
    
        myLabel1.grid(row = 0, column = 0)
        myLabel2.grid(row = 0, column = 1)
        myLabel3.grid(row = 0, column = 2)
        myLabel4.grid(row = 1, column = 0)
        myLabel5.grid(row = 1, column = 1)
        myLabel6.grid(row = 1, column = 2)
        
        #label = tk.Label(self.root, text="Hello World")
        #label.pack()
        
        self.root.mainloop()
    
    def setVals(self, v1,v2,v3):
        self.s4.set(str(v1))
        self.s5.set(str(v2))
        self.s6.set(str(v3))



app = App()
#print('Now we can continue running code while mainloop runs!')



while True:
    v_digital = np.uint16(sampleADC())
    logV_dig = math.log10(v_digital)
    lwFactor = getFactor(logV_dig, thresholdScale)
    app.setVals(v_digital, logV_dig, lwFactor)
    
    
#print(plt.get_backend())
#root.iconbitmap('a_path')
#myLabel.pack()