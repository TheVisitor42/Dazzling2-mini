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
#---------------
# DAZZLING2-MINI RECEIVER
#---------------
uart = UART(
    0,
    baudrate=BAUD_RATE,
    tx=Pin(0),
    rx=Pin(1)
)

buffer = b""
current_news_stories = []


# ========================================
# CLOCK STATE
# ========================================

clock_year = 0
clock_month = 0
clock_day = 0

clock_hour = 0
clock_minute = 0
clock_second = 0

clock_last_update = 0
clock_synchronized = False


# ========================================
# NEXT EVENT DISPLAY STATE
# ========================================

next_event_time = "--:--"
next_event_date = "--/--/----"
next_event_label = "WAITING FOR SCHEDULE"

next_event_received = False

# OLED #3 shows:
# - Clock for 25 seconds
# - Next event reminder for 5 seconds
# - Repeat every 30 seconds

DISPLAY_CYCLE_MS = 30000
REMINDER_DURATION_MS = 5000

display_cycle_start = time.ticks_ms()
reminder_is_visible = False


def receive_packet():

    global buffer

    if uart.any():

        received_data = uart.read()

        if received_data:
            buffer += received_data

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


# ========================================
# CLOCK FUNCTIONS
# ========================================

def start_clock(packet):

    global clock_year
    global clock_month
    global clock_day

    global clock_hour
    global clock_minute
    global clock_second

    global clock_last_update
    global clock_synchronized

    clock_string = packet["data"]["datetime"]
    date_string = packet["data"]["date"]

    # Time is HH:MM:SS
    time_parts = clock_string.split(":")

    clock_hour = int(time_parts[0])
    clock_minute = int(time_parts[1])
    clock_second = int(time_parts[2])

    # Date is MM/DD/YYYY
    date_parts = date_string.split("/")

    clock_month = int(date_parts[0])
    clock_day = int(date_parts[1])
    clock_year = int(date_parts[2])

    clock_last_update = time.ticks_ms()

    clock_synchronized = True

    # Update the clock only when its page is visible.
    if not reminder_is_visible:
        display_clock()

    print("Clock synchronized:")
    print(
        "{:02d}:{:02d}:{:02d}".format(
            clock_hour,
            clock_minute,
            clock_second
        )
    )

    print(
        "{:02d}/{:02d}/{:04d}".format(
            clock_month,
            clock_day,
            clock_year
        )
    )


def increment_clock():

    global clock_year
    global clock_month
    global clock_day

    global clock_hour
    global clock_minute
    global clock_second

    clock_second += 1

    if clock_second >= 60:

        clock_second = 0
        clock_minute += 1

    if clock_minute >= 60:

        clock_minute = 0
        clock_hour += 1

    if clock_hour >= 24:

        clock_hour = 0
        clock_day += 1

    # Days in each month.
    days_in_month = [
        31,
        28,
        31,
        30,
        31,
        30,
        31,
        31,
        30,
        31,
        30,
        31
    ]

    # Leap year correction.
    if (
        clock_year % 4 == 0 and
        (
            clock_year % 100 != 0 or
            clock_year % 400 == 0
        )
    ):

        days_in_month[1] = 29

    if clock_day > days_in_month[clock_month - 1]:

        clock_day = 1
        clock_month += 1

    if clock_month > 12:

        clock_month = 1
        clock_year += 1


def update_clock():

    global clock_last_update

    if not clock_synchronized:
        return

    now = time.ticks_ms()

    elapsed = time.ticks_diff(
        now,
        clock_last_update
    )

    # Advance once for every elapsed second.
    while elapsed >= 1000:

        increment_clock()

        clock_last_update = time.ticks_add(
            clock_last_update,
            1000
        )

        elapsed = time.ticks_diff(
            now,
            clock_last_update
        )

        # Don't overwrite the reminder with the clock.
        if not reminder_is_visible:
            display_clock()


def display_clock():

    if not clock_synchronized:

        display_text(
            3,
            "CLOCK",
            "WAITING",
            "FOR NTP"
        )

        return

    display_text(
        3,
        "CLOCK",
        "{:02d}:{:02d}:{:02d}".format(
            clock_hour,
            clock_minute,
            clock_second
        ),
        "{:02d}/{:02d}/{:04d}".format(
            clock_month,
            clock_day,
            clock_year
        )
    )


# ========================================
# NEXT EVENT REMINDER
# ========================================

def display_next_event(packet):

    global next_event_time
    global next_event_date
    global next_event_label
    global next_event_received

    data = packet["data"]

    next_event_time = data.get(
        "time",
        "--:--"
    )

    next_event_date = data.get(
        "date",
        "--/--/----"
    )

    next_event_label = data.get(
        "label",
        "SCHEDULED UPDATE"
    )

    next_event_received = True

    print("Next event received:")
    print("Time:", next_event_time)
    print("Date:", next_event_date)
    print("Event:", next_event_label)

    # Don't force the reminder onto the screen here.
    # The timed display cycle decides when it appears.


def show_next_event():

    display_text(
        3,
        "NEXT UPDATE AT",
        next_event_time,
        next_event_date,
        next_event_label
    )


def update_display_cycle():

    global display_cycle_start
    global reminder_is_visible

    now = time.ticks_ms()

    elapsed = time.ticks_diff(
        now,
        display_cycle_start
    )

    # Start a new 30-second cycle when necessary.
    if elapsed >= DISPLAY_CYCLE_MS:

        display_cycle_start = time.ticks_add(
            display_cycle_start,
            (elapsed // DISPLAY_CYCLE_MS)
            * DISPLAY_CYCLE_MS
        )

        elapsed = time.ticks_diff(
            now,
            display_cycle_start
        )

    # First 25 seconds: clock.
    if elapsed < (
        DISPLAY_CYCLE_MS - REMINDER_DURATION_MS
    ):

        if reminder_is_visible:

            reminder_is_visible = False
            display_clock()

    # Last 5 seconds: next event reminder.
    else:

        if (
            not reminder_is_visible
            and next_event_received
        ):

            reminder_is_visible = True
            show_next_event()


# ========================================
# OTHER DISPLAYS
# ========================================

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


# ========================================
# STARTUP
# ========================================

print("Starting OLEDs...")

initialize_oleds()

print("OLEDs initialized.")

display_clock()

print("Waiting for UART packet...")


# ========================================
# MAIN LOOP
# ========================================

while True:

    packet = receive_packet()

    if packet is not None:

        print()
        print("Packet received:")
        print(packet)

        received_sequence = packet["meta"]["sequence"]

        print("Sequence:", received_sequence)

        if packet["mode"] == "clock":

            start_clock(packet)

        elif packet["mode"] == "next_event":

            display_next_event(packet)

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

    update_clock()

    update_display_cycle()

    update_news()

    time.sleep_ms(10)


