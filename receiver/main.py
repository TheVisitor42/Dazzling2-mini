from machine import UART, Pin
import time
from shared.constants import BAUD_RATE

uart = UART(
    0,
    baudrate=BAUD_RATE,
    tx=Pin(0),
    rx=Pin(1)
)

print("---------------Receiver started---------------")
def receive_packet():
    while True:
        if uart.any():
            data = uart.read()
            print(data)
            print(len(data), data)

        time.sleep(0.25)
    
    #the UART buffer is only 256 bytes
    
