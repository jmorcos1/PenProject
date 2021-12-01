from thinkpenImports2 import *

# Data collection setup
RATE = 860
SAMPLES = 50

# Create the I2C bus with a fast frequency
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
    data = np.array(([0] * SAMPLES), dtype="int16")
    start = time.monotonic()
    time_next_sample = start + sample_interval
    # Read the same channel over and over
    for i in range(SAMPLES):
        # Wait for expected conversion finish time
        while time.monotonic() < (time_next_sample):
            pass
        # Read conversion value for ADC channel
        data[i] = chan0.value
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
    return math.floor(sum(data)/len(data))

def getFactor(val, threshDict):
    for thr in reversed(list(threshDict.keys())):
        if val > float(thr):
            return threshDict[thr]
    return 0

def getContact_getSize():
    v_digital = np.uint16(sampleADC())
    logV_dig = math.log10(v_digital)
    lwFactor = getFactor(logV_dig, thresholdScale)
    inContact = lwFactor > 0
    return [inContact, lwFactor]

def calibrateMin():
    print('Calibrating - do not touch')
    time.sleep(3)
    v_digital = np.uint16(sampleADC())
    logV_dig = math.log10(v_digital)
    print('done calibrating')
    return logV_dig*1.008



sFactorIn = 0.2
nFactors = 14
sFactor = sFactorIn
#minThresh = 3.781
minThresh = calibrateMin()
expectedRange = 0.18
maxThresh = minThresh + expectedRange 
factorScale = np.array([sFactor])

while len(factorScale) < nFactors:
    sFactor *= 1.2
    factorScale = np.append(factorScale, sFactor)

thresholdScale = dict(zip(np.around(np.linspace(minThresh, maxThresh, nFactors), 3), np.around(factorScale, 3)))
#print(thresholdScale)