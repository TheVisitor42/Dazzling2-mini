from machine import UART, Pin
import time
from shared.constants import BAUD_RATE
import json
import wifi

from event_executor import EventExecutor

#How to run this code (SENDER) with its sister code (RECEIVER)
#Step 1. Open this code and run it.
#Step 2. Close the code but don't stop it.
#Step 3. Switch to using the other Pico
#Step 4. Open and run the main.py for the RECEIVER Pico.
#Step 5. Wait for shell output.


#Give self time to switch to the Receiver Pico terminal and turn it on before the Sender Pico starts sending data over UART lines.
time.sleep(10)


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
# Build Packet
# -------------------------------------------------

def build_packet(mode, data=None):

    global sequence_number

    if mode == "clock": #CLOCK MODE

        now = time.localtime()

        packet = {
            "type": "data",

            "mode": "clock",

            "data": {
                "datetime": "{:04d}.{:02d}.{:02d} {:02d}:{:02d}".format(
                    now[0],
                    now[1],
                    now[2],
                    now[3],
                    now[4]
                )
            },

            "meta": {
                "version": 1,
                "sequence": sequence_number
            }
        }

    elif mode == "weather": #WEATHER MODE

        packet = {
            "type": "data",

            "mode": "weather",

            "data": data,

            "meta": {
                "version": 1,
                "sequence": sequence_number
            }
        }
    
    elif mode == "stocks": #STOCK MODE

        packet = {
            "type": "data",

            "mode": "stocks",

            "data": {
                "BRK.B": {
                    "price": 500,
                    "change": 2.31
                },
                "NTDOY": {
                    "price": 11.01,
                    "change": -1.01
                }
            },

            "meta": {
                "version": 1,
                "sequence": sequence_number
            }
        }
        
    elif mode == "news": #NEWS MODE

        packet = {
            "type": "data",

            "mode": "news",

            "data": {
                "top_stories": [
                    "Rich bastards meet with Xi and the homies",
                    "Dazzling2-mini development continues. Next stop all four screens working at the same time demo."
]
            },

            "meta": {
                "version": 1,
                "sequence": sequence_number
            }
        }
    
  
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
# Wi-Fi
# -------------------------------------------------

if not wifi.connect():

    print("WiFi connection failed.")
    print("Stopping program.")

    while True:
        time.sleep(10)

# -------------------------------------------------
# Event Executor
# -------------------------------------------------

executor = EventExecutor()


# -------------------------------------------------
# Main Loop
# -------------------------------------------------

while True:

    print()
    print("================================")
    print("RUNNING WEATHER TEST")
    print("================================")

    event = {
        "event": "weather",
        "profile": "WEATHER_A"
    }

    result = executor.execute(event)

    if result["success"] and result["update"]:

        print()
        print("Building weather packet...")

        packet = build_packet(
            "weather",
            result["data"]
        )

        send_packet(packet)

        print()
        print("Weather packet sent.")

    else:

        print()
        print("Weather update failed.")
        print("Error:", result["error"])

    time.sleep(90)

