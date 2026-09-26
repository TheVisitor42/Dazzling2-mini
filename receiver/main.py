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


# -------------------------------------------------
# UART
# -------------------------------------------------

uart = UART(
    0,
    baudrate=BAUD_RATE,
    tx=Pin(0),
    rx=Pin(1)
)


buffer = b""


# -------------------------------------------------
# News Tracking
# -------------------------------------------------

# Stores the most recently received stories.
# This prevents the same news packet from
# restarting the paging cycle.
current_news_stories = []


# -------------------------------------------------
# Receive Packet
# -------------------------------------------------

def receive_packet():

    global buffer

    if uart.any():

        buffer += uart.read()

        if b"\n" in buffer:

            packet_bytes, buffer = buffer.split(b"\n", 1)

            try:

                packet_string = packet_bytes.decode("utf-8")

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


# -------------------------------------------------
# Initialize OLEDs
# -------------------------------------------------

print("Starting OLEDs...")

initialize_oleds()

print("OLEDs initialized.")
print("Waiting for UART packet...")


# -------------------------------------------------
# Clock
# -------------------------------------------------

def display_clock(packet):

    clock = packet["data"]["datetime"]

    display_text(
        3,
        clock
    )

    print("Clock displayed on OLED #3")


# -------------------------------------------------
# Stocks
# -------------------------------------------------

def display_stocks(packet):

    stocks = packet["data"]

    brk = stocks["BRK.B"]
    ntdoy = stocks["NTDOY"]

    display_text(
        1,
        "STOCKS",
        "BRK.B $" + str(brk["price"]),
        "NTDOY $" + str(ntdoy["price"]),
        "CHG " + str(brk["change"]) + " / " + str(ntdoy["change"])
    )

    print("Stocks displayed on OLED #1")


# -------------------------------------------------
# Weather
# -------------------------------------------------

def display_weather(packet):

    weather = packet["data"]

    display_text(
        0,
        "WEATHER",
        "TEMP " + str(weather["temperature"]),
        "WIND " + str(weather["wind_speed"]),
        "RAIN " + str(weather["precipitation"])
    )

    print("Weather displayed on OLED #0")


# -------------------------------------------------
# Main Loop
# -------------------------------------------------

while True:

    packet = receive_packet()

    if packet is not None:

        print("Packet received:")
        print(packet)

        received_sequence = packet["meta"]["sequence"]

        print("Sequence:", received_sequence)

        # -----------------------------------------
        # Clock
        # -----------------------------------------

        if packet["mode"] == "clock":

            display_clock(packet)


        # -----------------------------------------
        # Stocks
        # -----------------------------------------

        elif packet["mode"] == "stocks":

            display_stocks(packet)


        # -----------------------------------------
        # News
        # -----------------------------------------

        elif packet["mode"] == "news":

            stories = packet["data"]["top_stories"]

            # Only restart the news display if the
            # actual stories have changed.
            if stories != current_news_stories:

                current_news_stories = stories

                start_news(stories)

                print("New news loaded")

            else:

                print("Same news received - continuing current pages")


        # -----------------------------------------
        # Weather
        # -----------------------------------------

        elif packet["mode"] == "weather":

            display_weather(packet)


    # ---------------------------------------------
    # Keep News Paging Running
    # ---------------------------------------------

    update_news()

    time.sleep_ms(10)
