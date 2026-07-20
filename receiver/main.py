from machine import UART, Pin
import time
import json
from shared.constants import BAUD_RATE


# -------------------------------------------------
# UART Initialization
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

buffer = b""

expected_sequence = 0


# -------------------------------------------------
# Receive One Packet
# -------------------------------------------------

def receive_packet():

    global buffer

    if uart.any():

        buffer += uart.read()

        # Wait until a complete packet arrives
        if b"\n" in buffer:

            packet_bytes, buffer = buffer.split(b"\n", 1)

            packet_string = packet_bytes.decode()

            packet = json.loads(packet_string)

            return packet

    return None


# -------------------------------------------------
# Sequence Number Check
# -------------------------------------------------

def check_sequence(packet):

    global expected_sequence

    received = packet["meta"]["sequence"]

    if received != expected_sequence:

        print("--------------------------------")
        print("Missing packet detected!")
        print("Expected:", expected_sequence)
        print("Received:", received)
        print("--------------------------------")

        expected_sequence = received + 1

        return True

    expected_sequence += 1

    return False


# -------------------------------------------------
# Main Program
# -------------------------------------------------

print("Receiver started...\n")




def display_weather(packet):

    weather = packet["data"]

    print('TEMP:',weather["temperature"])
    print('WIND SPEED:',weather["wind_speed"])
    print('Sunrise:',weather["sunrise"])
    print('Sunset:',weather["sunset"])
    print('Percipitation:',weather["percipitation"])

#customize displays here.

def display_stocks(packet):

    stocks = packet["data"]
    print("Packet received")
        print("Type:", packet["type"])
        print("Mode:", packet["mode"])
    print(stocks["BRK.B"]["price"])

def display_news(packet):
    news = packet["data"]

    print(news["top_stories"])

elif display_clock(packet):

    clock = packet["data"]

    print(clock["time"])
else:

    unkown = packet["data"]

    print(unkown["debug"])
    
#Process packet
def process_packet(packet):

    mode = packet["mode"]

    if mode == "weather":
        display_weather(packet)

    elif mode == "stocks":
        display_stocks(packet)

    elif mode == "news":
        display_news(packet)

    elif mode == "clock":
        display_clock(packet)

    else:
        print("Unknown mode:", mode)

'''    
#old while true loop
while True:

    packet = receive_packet()

    if packet is not None:

        missing = check_sequence(packet)

        print("Packet received")
        print("Type:", packet["type"])
        print("Mode:", packet["mode"])
        print("Sequence:", packet["meta"]["sequence"])
        print(packet)
        print("--------------------------------")

        if missing:
            # Future:
            # send_error_packet()
            # request_resend()
            pass

    time.sleep(0.01)
'''

#new while true loop

while True:

    packet = receive_packet()

    if packet is not None:

        missing = check_sequence(packet)

        if not missing:

            process_packet(packet)

    time.sleep(0.01)


    
