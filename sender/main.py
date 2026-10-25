from machine import UART, Pin
import time
import json

from shared.constants import BAUD_RATE
import wifi

from scheduler import Scheduler
from event_executor import EventExecutor


# -------------------------------------------------
# STARTUP
# -------------------------------------------------

print("================================")
print("DAZZLING2-MINI SENDER")
print("================================")

time.sleep(19)


# -------------------------------------------------
# UTC TO CENTRAL TIME
# -------------------------------------------------

def is_central_daylight_time(utc_time):
    """
    Determine whether a UTC timestamp falls within
    US Central Daylight Time.
    """

    year = utc_time[0]

    # Find the second Sunday in March.
    march_first = time.mktime(
        (year, 3, 1, 0, 0, 0, 0, 0)
    )

    march_weekday = time.localtime(march_first)[6]

    second_sunday_march = (
        1 + ((6 - march_weekday) % 7) + 7
    )

    # Find the first Sunday in November.
    november_first = time.mktime(
        (year, 11, 1, 0, 0, 0, 0, 0)
    )

    november_weekday = time.localtime(november_first)[6]

    first_sunday_november = (
        1 + ((6 - november_weekday) % 7)
    )

    month = utc_time[1]
    day = utc_time[2]
    hour = utc_time[3]

    if month < 3:
        return False

    if 3 < month < 11:
        return True

    if month > 11:
        return False

    # March: DST begins at 08:00 UTC.
    if month == 3:

        if day > second_sunday_march:
            return True

        if day < second_sunday_march:
            return False

        return hour >= 8

    # November: DST ends at 07:00 UTC.
    if month == 11:

        if day < first_sunday_november:
            return True

        if day > first_sunday_november:
            return False

        return hour < 7

    return False


def get_central_time():
    """
    Convert UTC system time to Central Time.
    Returns a time.localtime()-compatible tuple.
    """

    utc_time = time.gmtime()

    if is_central_daylight_time(utc_time):
        offset_hours = -5
    else:
        offset_hours = -6

    utc_seconds = time.mktime(utc_time)

    central_seconds = (
        utc_seconds + offset_hours * 3600
    )

    return time.localtime(central_seconds)


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
# GLOBAL VARIABLES
# -------------------------------------------------

sequence_number = 0
scheduled_events = []


# -------------------------------------------------
# BUILD PACKETS
# -------------------------------------------------

def build_packet(mode, data):

    global sequence_number

    packet = {
        "type": "data",
        "mode": mode,
        "data": data,
        "meta": {
            "version": 1,
            "sequence": sequence_number
        }
    }

    sequence_number += 1

    return packet


def build_clock_packet(data):

    central = data["central_time"]

    clock_data = {
        "datetime": "{:02d}:{:02d}:{:02d}".format(
            central[3],
            central[4],
            central[5]
        ),
        "date": "{:02d}/{:02d}/{:04d}".format(
            central[1],
            central[2],
            central[0]
        )
    }

    return build_packet(
        "clock",
        clock_data
    )


# -------------------------------------------------
# SEND PACKETS
# -------------------------------------------------

def send_packet(packet):

    json_message = json.dumps(packet) + "\n"

    print()
    print("Sending packet:")
    print(json_message)

    uart.write(json_message.encode())

    print("Packet sent.")


# -------------------------------------------------
# CONNECT TO WI-FI
# -------------------------------------------------

if not wifi.connect():

    print("Wi-Fi connection failed.")
    print("Stopping program.")

    while True:
        time.sleep(10)


# -------------------------------------------------
# CREATE EVENT EXECUTOR
# -------------------------------------------------

executor = EventExecutor()


# -------------------------------------------------
# INITIAL CLOCK SYNCHRONIZATION
# -------------------------------------------------

print()
print("Synchronizing Sender clock...")

initial_clock_event = {
    "event": "clock",
    "profile": "CLOCK"
}

initial_clock_result = executor.execute(
    initial_clock_event
)

if (
    initial_clock_result["success"]
    and initial_clock_result["update"]
):

    clock_packet = build_clock_packet(
        initial_clock_result["data"]
    )

    send_packet(clock_packet)

else:

    print("Initial clock synchronization failed.")
    print("Scheduled clock synchronization can retry later.")


# -------------------------------------------------
# INITIAL WEATHER FETCH
# -------------------------------------------------

print()
print("================================")
print("STARTUP WEATHER UPDATE")
print("================================")

initial_weather_event = {
    "event": "weather",
    "profile": "WEATHER_A"
}

initial_weather_result = executor.execute(
    initial_weather_event
)

if (
    initial_weather_result["success"]
    and initial_weather_result["update"]
):

    print()
    print("Startup weather fetch successful.")

    weather_packet = build_packet(
        "weather",
        initial_weather_result["data"]
    )

    send_packet(weather_packet)

else:

    print()
    print("Startup weather fetch failed.")

    print(
        "Error:",
        initial_weather_result["error"]
    )

    print("The scheduler will continue running.")


# -------------------------------------------------
# BUILD WEEKLY SCHEDULE
# -------------------------------------------------

scheduler = Scheduler()


def add_event(
    weekday,
    hour,
    minute,
    event,
    profile
):

    scheduler.add_weekly_event(
        weekday,
        hour,
        minute,
        event,
        profile
    )

    scheduled_events.append({
        "weekday": weekday,
        "hour": hour,
        "minute": minute,
        "event": event,
        "profile": profile
    })


# MONDAY

add_event(Scheduler.MONDAY, 6, 59, "clock", "CLOCK")
add_event(Scheduler.MONDAY, 7, 0, "weather", "WEATHER_A")
add_event(Scheduler.MONDAY, 7, 0, "news", "NEWS_A")
add_event(Scheduler.MONDAY, 9, 0, "stocks", "STOCKS_A")
add_event(Scheduler.MONDAY, 12, 0, "weather", "WEATHER_A")
add_event(Scheduler.MONDAY, 16, 0, "stocks", "STOCKS_A")
add_event(Scheduler.MONDAY, 18, 0, "weather", "WEATHER_B")
add_event(Scheduler.MONDAY, 18, 0, "stocks", "STOCKS_B")


# TUESDAY

add_event(Scheduler.TUESDAY, 6, 59, "clock", "CLOCK")
add_event(Scheduler.TUESDAY, 7, 0, "weather", "WEATHER_A")
add_event(Scheduler.TUESDAY, 7, 0, "news", "NEWS_B")
add_event(Scheduler.TUESDAY, 9, 0, "stocks", "STOCKS_A")
add_event(Scheduler.TUESDAY, 12, 0, "weather", "WEATHER_A")
add_event(Scheduler.TUESDAY, 16, 0, "stocks", "STOCKS_A")


# WEDNESDAY

add_event(Scheduler.WEDNESDAY, 6, 59, "clock", "CLOCK")
add_event(Scheduler.WEDNESDAY, 7, 0, "weather", "WEATHER_A")
add_event(Scheduler.WEDNESDAY, 7, 0, "news", "NEWS_B")
add_event(Scheduler.WEDNESDAY, 9, 0, "stocks", "STOCKS_A")
add_event(Scheduler.WEDNESDAY, 9, 0, "weather", "WEATHER_B")
add_event(Scheduler.WEDNESDAY, 12, 0, "weather", "WEATHER_A")
add_event(Scheduler.WEDNESDAY, 16, 0, "stocks", "STOCKS_A")
add_event(Scheduler.WEDNESDAY, 16, 0, "news", "NEWS_C")
add_event(Scheduler.WEDNESDAY, 18, 0, "news", "NEWS_A")
add_event(Scheduler.WEDNESDAY, 18, 0, "stocks", "STOCKS_C")


# THURSDAY

add_event(Scheduler.THURSDAY, 6, 59, "clock", "CLOCK")
add_event(Scheduler.THURSDAY, 7, 0, "weather", "WEATHER_A")
add_event(Scheduler.THURSDAY, 7, 0, "news", "NEWS_B")
add_event(Scheduler.THURSDAY, 9, 0, "stocks", "STOCKS_A")
add_event(Scheduler.THURSDAY, 12, 0, "weather", "WEATHER_A")
add_event(Scheduler.THURSDAY, 16, 0, "stocks", "STOCKS_A")
add_event(Scheduler.THURSDAY, 16, 0, "news", "NEWS_C")
add_event(Scheduler.THURSDAY, 18, 0, "news", "NEWS_A")
add_event(Scheduler.THURSDAY, 18, 0, "weather", "WEATHER_A")


# FRIDAY

add_event(Scheduler.FRIDAY, 6, 59, "clock", "CLOCK")
add_event(Scheduler.FRIDAY, 7, 0, "weather", "WEATHER_A")
add_event(Scheduler.FRIDAY, 9, 0, "stocks", "STOCKS_A")
add_event(Scheduler.FRIDAY, 12, 0, "weather", "WEATHER_A")
add_event(Scheduler.FRIDAY, 12, 0, "news", "NEWS_A")
add_event(Scheduler.FRIDAY, 16, 0, "stocks", "STOCKS_A")
add_event(Scheduler.FRIDAY, 18, 0, "weather", "WEATHER_A")
add_event(Scheduler.FRIDAY, 18, 0, "stocks", "STOCKS_B")


# SATURDAY

add_event(Scheduler.SATURDAY, 6, 59, "clock", "CLOCK")
add_event(Scheduler.SATURDAY, 7, 0, "weather", "WEATHER_A")
add_event(Scheduler.SATURDAY, 7, 0, "news", "NEWS_B")
add_event(Scheduler.SATURDAY, 12, 0, "weather", "WEATHER_A")
add_event(Scheduler.SATURDAY, 12, 0, "news", "NEWS_A")
add_event(Scheduler.SATURDAY, 19, 0, "weather", "WEATHER_A")
add_event(Scheduler.SATURDAY, 19, 0, "news", "NEWS_C")


# SUNDAY

add_event(Scheduler.SUNDAY, 6, 59, "clock", "CLOCK")
add_event(Scheduler.SUNDAY, 7, 0, "weather", "WEATHER_A")
add_event(Scheduler.SUNDAY, 7, 0, "news", "NEWS_A")
add_event(Scheduler.SUNDAY, 11, 0, "weather", "WEATHER_B")
add_event(Scheduler.SUNDAY, 11, 0, "news", "NEWS_B")
add_event(Scheduler.SUNDAY, 15, 0, "weather", "WEATHER_A")
add_event(Scheduler.SUNDAY, 22, 0, "news", "NEWS_C")


# -------------------------------------------------
# NEXT EVENT REMINDER
# -------------------------------------------------

def get_event_label(events):

    labels = []

    for event in events:

        if event["event"] == "clock":
            label = "CLOCK SYNC"

        elif event["event"] == "weather":
            label = "WEATHER"

        elif event["event"] == "news":
            label = "NEWS"

        elif event["event"] == "stocks":
            label = "STOCKS"

        else:
            label = event["event"].upper()

        if label not in labels:
            labels.append(label)

    return " + ".join(labels)


def get_next_event(current_time):

    current_weekday = current_time[6]
    current_hour = current_time[3]
    current_minute = current_time[4]

    current_minutes = (
        current_hour * 60 + current_minute
    )

    best_minutes_ahead = None
    best_event_time = None

    for event in scheduled_events:

        days_ahead = (
            event["weekday"] - current_weekday
        ) % 7

        event_minutes = (
            event["hour"] * 60 + event["minute"]
        )

        minutes_ahead = (
            days_ahead * 1440
            + event_minutes
            - current_minutes
        )

        # If today's event time has passed,
        # look for its occurrence next week.
        if minutes_ahead <= 0:
            minutes_ahead += 7 * 1440

        if (
            best_minutes_ahead is None
            or minutes_ahead < best_minutes_ahead
        ):

            best_minutes_ahead = minutes_ahead

            best_event_time = {
                "weekday": event["weekday"],
                "hour": event["hour"],
                "minute": event["minute"],
                "minutes_ahead": minutes_ahead
            }

    if best_event_time is None:
        return None

    # Gather all events at the same weekday and time.
    matching_events = []

    for event in scheduled_events:

        if (
            event["weekday"]
            == best_event_time["weekday"]
            and event["hour"]
            == best_event_time["hour"]
            and event["minute"]
            == best_event_time["minute"]
        ):

            matching_events.append(event)

    # Calculate the next event's calendar date.
    current_epoch = time.mktime(current_time)

    event_epoch = (
        current_epoch
        + best_event_time["minutes_ahead"] * 60
    )

    event_date = time.localtime(event_epoch)

    hour = best_event_time["hour"]

    if hour == 0:
        display_hour = 12
        am_pm = "AM"

    elif hour < 12:
        display_hour = hour
        am_pm = "AM"

    elif hour == 12:
        display_hour = 12
        am_pm = "PM"

    else:
        display_hour = hour - 12
        am_pm = "PM"

    return {
        "time": "{}:{:02d} {}".format(
            display_hour,
            best_event_time["minute"],
            am_pm
        ),
        "date": "{:02d}/{:02d}/{}".format(
            event_date[1],
            event_date[2],
            event_date[0]
        ),
        "label": get_event_label(matching_events)
    }


def send_next_event():

    current_time = get_central_time()

    next_event = get_next_event(current_time)

    if next_event is None:

        print("No scheduled events available.")

        return

    print()
    print("NEXT SCHEDULED EVENT")
    print(next_event)

    packet = build_packet(
        "next_event",
        next_event
    )

    send_packet(packet)


# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------

print()
print("Scheduler running.")

# Send the first next-event reminder to the Receiver.
send_next_event()

# Resend the reminder every 10 seconds.
last_reminder_sent = time.ticks_ms()
REMINDER_RESEND_MS = 10000

last_reported_minute = None


while True:

    current_time = get_central_time()

    # Print the scheduler's time once per minute.
    current_minute = (
        current_time[0],
        current_time[1],
        current_time[2],
        current_time[3],
        current_time[4]
    )

    if current_minute != last_reported_minute:

        print(
            "Scheduler time (Central): "
            "{:04d}-{:02d}-{:02d} "
            "{:02d}:{:02d}".format(
                current_time[0],
                current_time[1],
                current_time[2],
                current_time[3],
                current_time[4]
            )
        )

        last_reported_minute = current_minute

    due_events = scheduler.check(
        current_time
    )

    for event in due_events:

        result = executor.execute(event)

        if not result["success"]:
            print("Event failed:", event)
            continue

        if not result["update"]:
            continue

        if event["event"] == "clock":

            packet = build_clock_packet(
                result["data"]
            )

            send_packet(packet)

        elif event["event"] == "weather":

            packet = build_packet(
                "weather",
                result["data"]
            )

            send_packet(packet)

        else:

            print(
                "No packet builder configured for:",
                event["event"]
            )

    if due_events:
        send_next_event()
        last_reminder_sent = time.ticks_ms()

    # Resend the reminder in case a UART packet was missed.
    now = time.ticks_ms()

    if time.ticks_diff(
        now,
        last_reminder_sent
    ) >= REMINDER_RESEND_MS:

        send_next_event()
        last_reminder_sent = time.ticks_ms()

    time.sleep(1)

