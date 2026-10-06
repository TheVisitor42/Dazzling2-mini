from machine import UART, Pin
import time
import json

from shared.constants import BAUD_RATE

from oled import (
    initialize_oleds,
    display_text,
    start_news,
    update_news
)


# =================================================
# UART
# =================================================

uart = UART(
    0,
    baudrate=BAUD_RATE,
    tx=Pin(0),
    rx=Pin(1)
)

buffer = b""


# =================================================
# Current Data
# =================================================

current_news_stories = []


# =================================================
# Receive Packet
# =================================================

def receive_packet():

    global buffer

    if uart.any():

        buffer += uart.read()

        if b"\n" in buffer:

            packet_bytes, buffer = buffer.split(
                b"\n",
                1
            )

            try:

                packet_string = packet_bytes.decode(
                    "utf-8"
                )

                return json.loads(packet_string)

            except UnicodeError:

                print("Bad UTF-8 packet:")
                print(packet_bytes)

                return None

            except ValueError:

                print("Bad JSON packet:")
                print(packet_bytes)

                return None

    return None


# =================================================
# Initialize OLEDs
# =================================================

print("Starting OLEDs...")

initialize_oleds()

print("OLEDs initialized.")
print("Waiting for UART packet...")


# =================================================
# Display Clock
# =================================================

def display_clock(packet):

    clock = packet["data"]["datetime"]

    display_text(
        3,
        "CLOCK",
        clock
    )

    print("Clock displayed on OLED #3")


# =================================================
# Display Stocks
# =================================================

def display_stocks(packet):

    stocks = packet["data"]

    brk = stocks["BRK.B"]
    ntdoy = stocks["NTDOY"]

    display_text(
        1,
        "STOCKS",
        "BRK.B $" + str(brk["price"]),
        "NTDOY $" + str(ntdoy["price"]),
        "CHG " + str(brk["change"]) +
        " / " +
        str(ntdoy["change"])
    )

    print("Stocks displayed on OLED #1")


# =================================================
# Display Weather
# =================================================

def display_weather(packet):

    weather = packet["data"]

    display_text(
        0,
        "WEATHER",
        "TEMP " + str(weather["temperature"]),
        "FEEL " + str(weather["feels_like"]),
        "WIND " + str(weather["wind_speed"]),
        "HUM " + str(weather["humidity"])
    )

    print("Weather displayed on OLED #0")


# =================================================
# Main Loop
# =================================================

while True:

    packet = receive_packet()

    if packet is not None:

        print()
        print("Packet received:")
        print(packet)

        received_sequence = packet["meta"]["sequence"]

        print("Sequence:", received_sequence)

        if packet["mode"] == "clock":

            display_clock(packet)

        elif packet["mode"] == "stocks":

            display_stocks(packet)

        elif packet["mode"] == "news":

            stories = packet["data"]["top_stories"]

            if stories != current_news_stories:

                current_news_stories = stories

                start_news(stories)

                print("New news loaded")

            else:

                print(
                    "Same news received - "
                    "continuing current pages"
                )

        elif packet["mode"] == "weather":

            display_weather(packet)

    # Keep news paging responsive
    update_news()

    time.sleep_ms(10)
