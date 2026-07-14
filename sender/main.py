#Sender-main.py

from machine import UART, Pin
import time
from shared.constants import BAUD_RATE

message = "Hello Pico!"

uart = UART(
    0,
    baudrate=BAUD_RATE,
    tx=Pin(0),
    rx=Pin(1)
)

while True:
    uart.write(message)
    time.sleep(1)