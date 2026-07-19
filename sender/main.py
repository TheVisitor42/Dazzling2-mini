from machine import UART, Pin
import time
from shared.constants import BAUD_RATE
import json


# -------------------------------------------------
# UART Connection
# -------------------------------------------------

uart = UART(
    0,
    baudrate=BAUD_RATE,
    tx=Pin(0),
    rx=Pin(1)
)


# -------------------------------------------------
# Global Variables
# -------------------------------------------------

sequence_number = 0


# -------------------------------------------------
# Save State Example (Not transmitted)
# -------------------------------------------------

save_state_data_example = {
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
            "date": "July 15",
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


# -------------------------------------------------
# Debug save_state_data_example
# -------------------------------------------------

print(save_state_data_example)
print(type(save_state_data_example))
print(len(save_state_data_example))

print("---------------------------------------------")


# -------------------------------------------------
# Build Packet
# -------------------------------------------------

def build_packet():

    global sequence_number

    packet = {
        "type": "data",

        "mode": "weather",

        "data": {
            "temperature": 76,
            "wind_speed": 5,
            "sunrise": "7:05 AM",
            "sunset": "7:30 PM",
            "precipitation": "4%"
        },

        "meta": {
            "version": 1,
            "sequence": sequence_number
        }
    }
    #debug
    print("Sequence:", packet["meta"]["sequence"])
    #increment sequence number
    
    sequence_number += 1

    return packet


# -------------------------------------------------
# Send Packet
# -------------------------------------------------

def send_packet(packet):

    # Packet debug

    print("Packet:")
    print(packet)
    print()

    print("Packet type:", type(packet))
    print("Top-level keys:", len(packet))
    print()

    # Convert dictionary to JSON

    json_message = json.dumps(packet)

    # Add packet terminator

    json_message += "\n"

    # JSON debug

    print("JSON:")
    print(json_message)
    print()

    print("JSON type:", type(json_message))
    print("JSON length:", len(json_message))
    print("---------------------------------------------")

    # Send packet

    uart.write(json_message.encode())


# -------------------------------------------------
# Main Loop
# -------------------------------------------------

while True:

    packet = build_packet()

    send_packet(packet)

    time.sleep(1)
