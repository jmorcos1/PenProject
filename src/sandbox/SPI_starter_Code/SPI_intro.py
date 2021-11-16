import time
import spidev


spi_ch = 0
spi = spidev.SpiDev(0, spi_ch)
spi.max_speed_hz = 2000000
#print ("SPI clock speed setting %s Hz" % spi.max_speed_hz)

print(spi.bits_per_word)

l = list(range(10))

foo = [1, 2, 3]

print(l)

print(foo)

