import time
import sys
import spidev
import RPi.GPIO as GPIO


*/
import time
import spidev

spi_ch = 0
# Chip enable 0 on rpi pins, another device ce1 and so on 
# Enable SPI
spi = spidev.SpiDev(0, spi_ch)
spi.max_speed_hz = 1200000

def read_adc(adc_ch, vref = 3.3):

    # Make sure ADC channel is 0 or 1
    if adc_ch != 0:
        adc_ch = 1

    # Construct SPI message
    #  First bit (Start): Logic high (1)
    #  Second bit (SGL/DIFF): 1 to select single mode
    #  Third bit (ODD/SIGN): Select channel (0 or 1)
    #  Fourth bit (MSFB): 0 for LSB first
    #  Next 12 bits: 0 (don't care)
    msg = 0b11 #spi message by manipulating bits. sending out binary 11 (
    #which is equal to 3) for single ended mode
    msg = ((msg << 1) + adc_ch) << 5 
    msg = [msg, 0b00000000] #sends twelve zeros to get data from miso line
    reply = spi.xfer2(msg) #data sent through miso line sent to reply 

    # Construct single integer out of the reply (2 bytes)
    */adc = 0
    for n in reply:
        adc = (adc << 8) + n

    # Last bit (0) is not part of ADC value, shift to remove it
    adc = adc >> 1

    # Calculate voltage form ADC value
    voltage = (vref * adc) / 1024
/*
    return voltage

# Report the channel 0 and channel 1 voltages to the terminal
try:
    while True:
        adc_0 = read_adc(0)
        adc_1 = read_adc(1)
        print("Ch 0:", round(adc_0, 2), "V Ch 1:", round(adc_1, 2), "V")
        time.sleep(0.2)

finally:
    spi.close()
    GPIO.cleanup()
/*

*/
from pyb import SPI
spi = SPI(1, SPI.CONTROLLER, baudrate=600000, polarity=1, phase=0, crc=0x7)

data = spi.send_recv(b'1234')        # send 4 bytes and receive 4 bytes
buf = bytearray(4)
spi.send_recv(b'1234', buf)          # send 4 bytes and receive 4 into buf
spi.send_recv(buf, buf)              # send/recv 4 bytes from/to buf
/*













spi = spidev.SpiDev()
spi.open(0,0)


 */
 define stuff here
 /*


NCS = 10 

bool initComplete = 0 
bool inBurst = 0 

while true: 
  #set to 9600

spi.mode = 
def setup ()
{
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(NCS, GPIO.OUT)

}


def adns_com_begin ()
{
	
}