#Sender-main.py

from machine import UART, Pin
import time
from shared.constants import BAUD_RATE


#Data Structure Example

system_data = {
    "modes": [
        "stocks",
        "weather",
        "news",
        "calendar",
        "clock",
        "reminders",
        "art",
        "diagnostics"
    ],

    "OLED": {

        "-stocks-": {
            "BRK.B": {
                "price": 500,
                "per_": 0.51,
                "pe_": 15,
                "name": "Berkshire Hathaway"
            },

            "NTDOY": {
                "price": 11.01,
                "per_": -1.01,
                "pe_": 17,
                "name": "Nintendo"
            }
        },

        "-weather-": {
            "temperature": 76,
            "wind_speed": 5,
            "direction": "NW",
            "sunrise": "6:51 AM",
            "sunset": "8:36 PM",
            "precipitation_%": 0.80,
            "raining": True
        },

        "-news-": {
            "top_stories": [
                "A cop a guy and a lady",
                "Honey badger does what it needs!"
            ]
        },

        "-calendar-": {
            "date":"July 15",
            "event": "dentist appt. 10AM"
        },

        "-clock-": "9:38 AM",

        "-reminders-": "Dinner with Gal tomorrow @ 5:30PM @ Grease Monkey"
    },


    "EINK": {

        "-art-": {
            "bitmap_array_Picaso_1": "11010X10011101",
            "name": "untitled",
            "medium": "charcoal on concrete"
        }
    },


    "-diagnostics-": {
        "cputemp": 38,
        "runtime": "10H30M10S",
        "droppedUART": None,
        "droppedAPI": None,
        "unexpectederr": 2
    },


    "meta": {
        "version": 1,
        "sequence": 0,

        "calls": {
            "stocks": [
                12,
                {
                    "BRK.B": 6,
                    "NTDOY": 6
                }
            ],
            "weather": 23,
            "news": 1,
            "calendar": 0,
            "clock": 3,
            "reminders": 0,
            "art": 5,
            "diagnostics": 0
        }
    }
}

print(system_data)

#UART Connection

message = "Hello Pico!"

uart = UART(
    0,
    baudrate=BAUD_RATE,
    tx=Pin(0),
    rx=Pin(1)
)

while True:
    uart.write(message)
    time.sleep(10)


