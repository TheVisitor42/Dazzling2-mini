from machine import UART, Pin
import time
import json

from shared.constants import BAUD_RATE
from oled import initialize_oleds, display_text


# -------------------------------------------------
# UART
# -------------------------------------------------

uart = UART(
    0,
    baudrate=BAUD_RATE,
    tx=Pin(0),
    rx=Pin(1)
)


# -------------------------------------------------
# UART Buffer
# -------------------------------------------------

buffer = b""
expected_sequence = 0


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
# Start OLEDs
# -------------------------------------------------

print("Starting OLEDs...")

initialize_oleds()

print("OLEDs initialized.")
print("Waiting for UART packet...")


# -------------------------------------------------
# Main Loop
# -------------------------------------------------

while True:

    packet = receive_packet()

    if packet is not None:

        print("Packet received:")
        print(packet)

        # Check sequence
        received_sequence = packet["meta"]["sequence"]

        print("Sequence:", received_sequence)

        # Only handle weather for this test
        if packet["mode"] == "weather":

            weather = packet["data"]

            display_text(
                0,
                "WEATHER",
                "TEMP " + str(weather["temperature"]),
                "WIND " + str(weather["wind_speed"]),
                "RAIN " + str(weather["precipitation"])
            )

            print("Weather displayed on OLED #0")

    time.sleep_ms(10)
