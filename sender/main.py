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

system_data = {
    "mode": "stocks",

    "stocks": {
        "BRK.B": {
            "price": 500,
            "per_change": 0.51
        },
        "NTDOY": {
            "price": 11.01,
            "per_change": -1.01
        }
    },

    "meta": {
        "version": 1,
        "sequence": 0
    }
}
