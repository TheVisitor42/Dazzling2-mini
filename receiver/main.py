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
