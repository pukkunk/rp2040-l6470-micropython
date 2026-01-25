# example/minimal.py
from machine import SPI, Pin
from l6470 import L6470
import time

spi = SPI(0, baudrate=1_000_000, polarity=1, phase=1, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
cs = Pin(5, Pin.OUT, value=1)
busy = Pin(0, Pin.IN)
motor = L6470(spi=spi, cs=cs, busy=busy)

motor.set_ACC(0x05)
motor.set_DEC(0x05)
motor.set_MAX_SPEED(0x200)
motor.run(L6470.FWD, 0x2000)

while True:
    time.sleep(1)
