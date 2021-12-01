from pmw_sensor_header import *
"""
#region
*This code was written to communicate with an optical navigation sensor
and us it to track the movements of a digital pen
*The positioning information will then be translated to commands using
the python Turtle library, to make digital drawings
*This code is based on code found on github page: 
https://github.com/SunjunKim/PMW3360_Arduino/blob/master/PMW3360DM-Burst/PMW3360DM-Burst.ino
-The arduino code was translated into python using CircuitPython libraries for SPI comm
*sensor datasheet:
https://d3s5r33r268y59.cloudfront.net/datasheets/9604/2017-05-07-18-19-11/PMS0058-PMW3360DM-T2QU-DS-R1.50-26092016._20161202173741.pdf
*Firmware file also given on the github page above
#endregion
"""

"""
SENSOR INFO:
----------------------------------------------------
#region
*PMW3360 on a Breakout Board (PCB)
-On-Board Power regulator - Compatable with 3.3V or 5V input
*Use 3.3v (PI pin 1)
-Max. Serial Port Clock Frequency: 2 MHz
-NCS is Active Low
-SPI Mode is 3 (b11)
-Speed of mouse sensor movement: Can handle up to 250 inches/second
-Up to 50 g of acceleration
#endregion
____________________________________________________
"""

#*PI Pinout SETUP
#--------------------------------------
#region
#SPI - Setup
#*Chip Select Pin
CS = digitalio.DigitalInOut(board.D25)
CS.direction = digitalio.Direction.OUTPUT
CS.value = True
#note - CS is toggled manually to start and end data transfer

#*connect to SPI device - create object and lock the bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
while not spi.try_lock():
    pass
spi.configure(baudrate=1000000, phase=1, polarity=1)

#TODO: deal with wires
#endregion
#_____________________________________________


#*setup parameters
#*CPI setting
#range is 100-12000
#?figure this out
#! Max is 12000
#CPI = 10000
CPI = 1600
"""
    #CPI = 6400
    #CPI = 3200
    #CPI = 1600
    #CPI = 5000 #default
"""
DELAY_TIME = 300/1000000 #just a delay of 300 µs

def pmw_WriteReg(addr, data):
    #input: 1 register address byte, 1 data byte
    #-performs a write to a given register
    #-data and addr should be unsigned bytes

    #mask - put a 1 in MSB (indicating a write op), followed by A_6-A_0 (address bits)
    regAddress = (addr | 0x80)
    #Bring CS low
    CS.value = False
    #Delay by T_ncs-slck before starting transmission
    time.sleep(T_NCS_SCLK/1000000000)
    #write function takes in: buffer - a bytearray
    spi.write(bytes([regAddress, data]))
    #Delay by T_slck-ncs before raising CS back to high
    time.sleep(T_SCLK_NCS_W/1000000)
    CS.value = True
    #Delay by minumum time between write and subsequent read or write
    time.sleep(DELAY_AFTER_WRITE)


def pmw_ReadReg(addr):
    #input: 1 register address byte
    #returns a byte read from that register

    #mask - put a O in MSB (indicating a read op), followed by A_6-A_0 (address bits)
    regAddress = (addr & 0x7F)
    #create buffer to store the read byte
    receive = bytearray(1)
    #bring CS low to start transaction
    CS.value = False
    #Delay by T_ncs_sclk before outputting address
    time.sleep(T_NCS_SCLK/1000000000)
    #transder freAdress byte
    spi.write(bytes([regAddress]))
    #delay by t_srad after sending address byte, before reading data
    time.sleep(T_SRAD/1000000)
    #read data into buffer
    spi.readinto(receive)
    #delay by t_slck_ncs before raising CS
    time.sleep(T_SCLK_NCS_R/1000000000)
    #end ransmission by raising CS back to high
    CS.value = True
    #delay by minumum time between read operation and subsequent read/write operation
    time.sleep(DELAY_AFTER_READ)
    #return the read byte
    return receive


def pmw_shutDown():
    DELAY_CS_TOGGLE = 2/1000000
    #reset the SPI port by toggling CS High then Low - then High again
    CS.value = True
    CS.value = False
    time.sleep(DELAY_CS_TOGGLE)
    CS.value = True
    #perform shutdown by writing 0xB6 to Shutdown Register
    shutdownMSG = bytes([SHUTDOWN, 0xB6])
    #pmw_WriteReg(np.ubyte(shutdownMSG[0]), np.ubyte(shutdownMSG[1]))
    pmw_WriteReg(shutdownMSG[0], shutdownMSG[1])


def pmw_powerUp():
    DELAY_CS_TOGGLE = 40/1000000
    DELAY_REBOOT = 50/1000000
    #reset the SPI port by toggling CS Low - then High again
    CS.value = False
    time.sleep(DELAY_CS_TOGGLE)
    CS.value = True
    time.sleep(DELAY_CS_TOGGLE)
    #force reset the mouse sensor
    resetMSG = bytes([POWER_UP_RESET, 0x5A])
    #pmw_WriteReg(np.ubyte(resetMSG[0]), np.ubyte(resetMSG[1]))
    pmw_WriteReg(resetMSG[0], resetMSG[1])
    time.sleep(DELAY_REBOOT)


def pmw_unRest():
    #Write 0 to Rest_En bit of Config2 register to disable Rest mode.
    message = bytes([CNFG2, 0x00])
    pmw_WriteReg(message[0], message[1])


def pmw_initSROM():
    #write 0x1d in SROM_enable reg for initializing
    FW_DELAY = 10/1000
    message = bytes([SROM_EN, 0x1D])
    pmw_WriteReg(message[0], message[1])
    #delay for more than one frame period
    time.sleep(FW_DELAY)


def pmw_startSROM_DL():
    #write 0x18 to SROM_enable to start SROM download
    message = bytes([SROM_EN, 0x18])
    pmw_WriteReg(message[0], message[1])

def displayRegisters(registers):
    for key in registers:
        regAddr = bytearray([registers[key]])
        readByte = pmw_ReadReg(regAddr[0])
        print(key, ': ', hex(readByte[0]))
    print("\n")


def performStartup():
    DELAY_FW = 10/1000000
    #shutdown the Mouse sensor
    pmw_shutDown()
    time.sleep(DELAY_TIME) #give it a sec
    #Power-up/Reset the Mouse sensor
    pmw_powerUp()
    #Read from registers 0x02 to 0x06 - part of chip initialiazation process
    targetRegisters = {
        'MOTION': MOTION,
        'DXL': DXL,
        'DXH': DXH,
        'DYL': DYL,
        'DYH': DYH
    }
    displayRegisters(targetRegisters)
    time.sleep(DELAY_FW)
    #upload the firmware
    pmw_uploadFW()
    time.sleep(DELAY_FW)
    setCPI(CPI)
    print("\n\t\t",'Mouse Sensor Initialized', "\n")


def pmw_uploadFW():
    FW_DELAY = 18/1000000
    FW_DELAY2 = 200/1000000
    print("uploading Firmware...")
    #disable rest mode
    pmw_unRest()
    #initialize SROM
    pmw_initSROM()
    #start the SROM download
    pmw_startSROM_DL()
    #Start by writing SROM_Load_burst destination address
    message = bytearray([(SROM_LOAD_BURST | 0x80)])
    #Drop CS to start transaction
    CS.value = False
    #Delay before sending data
    time.sleep(T_NCS_SCLK/1000000000)
    #Write the SROM load burst destination address
    spi.write(message)
    #delay before writing SROM file - as per datasheet instructions
    time.sleep(FW_DELAY)
    #send all bytes of firmware
    for byte in SROM.data:
        spi.write([byte])
        #required delay between SROM bytes
        time.sleep(FW_DELAY)
    #keep CS high for a short delay
    time.sleep(T_SCLK_NCS_W/1000000 - FW_DELAY)
    #End SROM transmission
    CS.value = True
    #delay by 200 µs before reading SROM ID
    time.sleep(FW_DELAY2)
    #read the SROM_ID for firmware version number - indicates successful FW DLoad
    regAddr = bytearray([SROM_ID])
    readByte = pmw_ReadReg(regAddr[0])
    print('SROM ID: ', hex(readByte[0]))
    #Write 0x00 to Config2 register for wired mouse or 0x20 for wireless mouse design
    message = bytearray([CNFG2, 0x00])
    pmw_WriteReg(message[0], message[1])


def setCPI(cpiVal):
  #set CPI
  myCPI =  int(cpiVal/100) - 1

  if(myCPI < 0):
    myCPI = 0
  elif(myCPI > 0x77):
    myCPI = 0x77

  cpiMessage = bytes([CNFG1, myCPI])
  pmw_WriteReg(cpiMessage[0], cpiMessage[1])
  time.sleep(DELAY_TIME)

  print('set CPI to: ', cpiVal)



def getDeltas():

    message = bytes([MOT_BURST, 0x00])
    pmw_WriteReg(message[0], message[1])
    CS.value = False
    burstBuffer = bytearray(12)
    spi.write(bytes([MOT_BURST]))
    time.sleep(T_SCLK_NCS_W/1000000)
    spi.readinto(burstBuffer)
    time.sleep(1/1000000)
    motionF = (burstBuffer[0] & 0x80) > 0
    liftF = (burstBuffer[0] & 0x08) > 0

    delta_xL = np.ubyte(burstBuffer[2])
    delta_xH = np.ubyte(burstBuffer[3])
    delta_yL = np.ubyte(burstBuffer[4])
    delta_yH = np.ubyte(burstBuffer[5])
    deltaX = np.short((delta_xH << 8) | delta_xL)
    deltaY = np.short(-1*((delta_yH << 8) | delta_yL))
    surfaceQ_in_numFeatures = 8*burstBuffer[6]
    CS.value = True
    time.sleep(1/1000000)

    """
    if(motionF):
        print('dX low:', delta_xL, bin(delta_xL))
        print('dX high:', delta_xH, bin(delta_xH))
        print('dY low:', delta_yL, bin(delta_yL))
        print('dY high:', delta_yH, bin(delta_yH))
        print('dX:', deltaX)
        print('dY:', deltaY)
    """
    return [motionF, deltaX, deltaY, surfaceQ_in_numFeatures, liftF]


def checkLiftConf():
    regAddr = bytes([LIFT_CONFIG])
    readByte = pmw_ReadReg(regAddr[0])
    print('Lift Config Setting: ', hex(readByte[0]))

def setLiftConf():
    regAddr = bytes([LIFT_CONFIG])
    readByte = pmw_ReadReg(regAddr[0])

    print(hex(readByte[0]))

    newSetting = (readByte[0] | 0x03)

    print(hex(newSetting))

    message = bytes([LIFT_CONFIG, newSetting])
    pmw_WriteReg(message[0], message[1])
    time.sleep(DELAY_TIME)
    


def checkSROM():
    FW_DELAY = 10/1000

    burstBuffer = bytearray(12)
    CS.value = False
    spi.write(bytes([(MOT_BURST | 0x80)]))
    time.sleep(T_SCLK_NCS_W/1000000)
    spi.readinto(burstBuffer)
    time.sleep(1/1000000)
    CS.value = True
    sromRunning = (burstBuffer[1] & 0x20) > 0
    print('SROM Running?: ', sromRunning)
    message = bytearray([SROM_EN, 0x15])
    pmw_WriteReg(message[0], message[1])
    time.sleep(FW_DELAY)
    regAddr = bytearray([DATA_OUT_U])
    readByte = pmw_ReadReg(regAddr[0])
    print('DOU: ', hex(readByte[0]))
    regAddr = bytearray([DATA_OUT_L])
    readByte = pmw_ReadReg(regAddr[0])
    print('DOL: ', hex(readByte[0]))

    checkLiftConf()
    setLiftConf()
    checkLiftConf()


def pmw_readMotion():
    #get accumulated motion (deltas) - not using burst
    message = bytes([MOTION, 0x00])
    pmw_WriteReg(message[0], message[1])

    regAddr = bytes([MOTION])
    readByte = pmw_ReadReg(regAddr[0])

    if(readByte[0] & 0x80 > 0):
        regAddr = bytes([DXL])
        deltaX_L = pmw_ReadReg(regAddr[0])
        regAddr = bytes([DXH])
        deltaX_H = pmw_ReadReg(regAddr[0])
        regAddr = bytes([DYL])
        deltaY_L = pmw_ReadReg(regAddr[0])
        regAddr = bytes([DYH])
        deltaY_H = pmw_ReadReg(regAddr[0])
        return [deltaX_L[0], deltaX_H[0], deltaY_L[0], deltaY_H[0]]
    else:
        return [0, 0, 0, 0]



def setUp():
    initComplete = False
    performStartup()
    time.sleep(1)
    targetRegisters = {
        'Product ID': PROD_ID,
        'Revision ID': REV_ID,
        'Inverse Product ID': INV_PROD_ID,
        'Firmware Version': SROM_ID,
        'MOTION register': MOTION
    }
    print('optical navigation sensor INFO: \n')
    displayRegisters(targetRegisters)
    regAddr = bytes([SROM_ID])
    readByte = pmw_ReadReg(regAddr[0])
    if(readByte[0] == 0x04):
        initComplete = True
    return initComplete

