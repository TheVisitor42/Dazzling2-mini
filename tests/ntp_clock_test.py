#NTP Clock Test is to be run on the Sender Pico.

import time
import json
from machine import UART, Pin
import ntptime

import wifi
from shared.constants import BAUD_RATE


uart = UART(
    0,
    baudrate=BAUD_RATE,
    tx=Pin(0),
    rx=Pin(1)
)


def central_time_from_utc(utc_time):
    """
    Convert UTC time to Central Time.

    2026 daylight-saving period:
    March 8 through November 1.
    """

    year = utc_time[0]

    # Second Sunday in March
    march_1 = time.mktime(
        (year, 3, 1, 0, 0, 0, 0, 0)
    )

    march_weekday = time.localtime(march_1)[6]

    days_to_sunday = (7 - march_weekday) % 7

    second_sunday = 1 + days_to_sunday + 7

    dst_start = time.mktime(
        (year, 3, second_sunday, 8, 0, 0, 0, 0)
    )

    # First Sunday in November
    november_1 = time.mktime(
        (year, 11, 1, 0, 0, 0, 0, 0)
    )

    november_weekday = time.localtime(november_1)[6]

    days_to_sunday = (7 - november_weekday) % 7

    first_sunday = 1 + days_to_sunday

    dst_end = time.mktime(
        (year, 11, first_sunday, 7, 0, 0, 0, 0)
    )

    utc_timestamp = time.mktime(utc_time)

    if dst_start <= utc_timestamp < dst_end:
        offset = -5 * 60 * 60
    else:
        offset = -6 * 60 * 60

    central_timestamp = utc_timestamp + offset

    return time.localtime(central_timestamp)


def build_clock_packet():
    now = central_time_from_utc(
        time.gmtime()
    )

    year = now[0]
    month = now[1]
    day = now[2]

    hour = now[3]
    minute = now[4]
    second = now[5]

    packet = {
        "mode": "clock",

        "meta": {
            "version": 1,
            "sequence": 0
        },

        "data": {
            "datetime":
                "{:02d}:{:02d}:{:02d}".format(
                    hour,
                    minute,
                    second
                ),

            "date":
                "{:02d}/{:02d}/{:04d}".format(
                    month,
                    day,
                    year
                )
        }
    }

    return packet


def send_packet(packet):

    packet_string = json.dumps(packet)

    uart.write(
        packet_string.encode("utf-8") + b"\n"
    )

    print()
    print("Packet sent:")
    print(packet_string)


print("================================")
print("NTP CLOCK TEST")
print("================================")

print()
print("Connecting to Wi-Fi...")

if not wifi.connect():

    print("Wi-Fi connection failed.")
    raise Exception("No Wi-Fi connection")


print()
print("Synchronizing with NTP...")

try:

    ntptime.settime()

    print("NTP synchronization successful.")

except Exception as e:

    print("NTP synchronization failed:")
    print(e)

    raise


print()
print("Current UTC:")
print(time.gmtime())

print()
print("Current Central Time:")

central = central_time_from_utc(
    time.gmtime()
)

print(
    "{:02d}:{:02d}:{:02d}".format(
        central[3],
        central[4],
        central[5]
    )
)

print(
    "{:02d}/{:02d}/{:04d}".format(
        central[1],
        central[2],
        central[0]
    )
)

print()
print("Sending clock packet...")

packet = build_clock_packet()

send_packet(packet)

print()
print("NTP CLOCK TEST COMPLETE.")
