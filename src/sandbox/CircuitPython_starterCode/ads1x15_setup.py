import math
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from adafruit_ads1x15.ads1x15 import Mode

# Data collection setup
RATE = 860
SAMPLES = 100
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

# First ADC channel read in continuous mode configures device
# and waits 2 conversion cycles
_ = chan0.value

sample_interval = 1.0 / ads.data_rate
repeats = 0
skips = 0

data = [None] * SAMPLES

start = time.monotonic()
time_next_sample = start + sample_interval

#print(chan.value, chan.voltage)

# Read the same channel over and over
for i in range(SAMPLES):
    # Wait for expected conversion finish time
    while time.monotonic() < (time_next_sample):
        pass

    # Read conversion value for ADC channel
    data[i] = chan0.value

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

rate_reported = SAMPLES / total_time
rate_actual = (SAMPLES - repeats) / total_time
# NOTE: leave input floating to pickup some random noise
#       This cannot estimate conversion rates higher than polling rate

print("Took {:5.3f} s to acquire {:d} samples.".format(total_time, SAMPLES))
print("")
print("Configured:")
print("    Requested       = {:5d}    sps".format(RATE))
print("    Reported        = {:5d}    sps".format(ads.data_rate))
print("")
print("Actual:")
print("    Polling Rate    = {:8.2f} sps".format(rate_reported))
print("                      {:9.2%}".format(rate_reported / RATE))
print("    Skipped         = {:5d}".format(skips))
print("    Repeats         = {:5d}".format(repeats))
print("    Conversion Rate = {:8.2f} sps   (estimated)".format(rate_actual))

#print(sum(data))
#print(sum(data)/len(data))
print(math.floor(sum(data)/len(data)))

#print(chan.value, chan.voltage)
