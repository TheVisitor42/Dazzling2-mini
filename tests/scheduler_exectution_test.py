# scheduler_execution_test.py
#
# Dazzling2-mini_2
# Sender Pico
#
# Tests continuous:
# Scheduler -> queued events -> sequential execution
#
# NO real APIs
# NO Wi-Fi
# NO UART


from scheduler import Scheduler
import time


# ============================================================
# CREATE SCHEDULER
# ============================================================

scheduler = Scheduler()


# Events scheduled close together.

scheduler.add_weekly_event(
    Scheduler.MONDAY,
    9,
    0,
    "stocks",
    "STOCKS_A"
)

scheduler.add_weekly_event(
    Scheduler.MONDAY,
    9,
    1,
    "weather",
    "WEATHER_A"
)

scheduler.add_weekly_event(
    Scheduler.MONDAY,
    9,
    2,
    "news",
    "NEWS_A"
)


# ============================================================
# FAKE API FUNCTIONS
# ============================================================

def fake_stocks_api():

    print()
    print("START STOCKS_A")

    time.sleep(3)

    print("FINISH STOCKS_A")


def fake_weather_api():

    print()
    print("START WEATHER_A")

    time.sleep(2)

    print("FINISH WEATHER_A")


def fake_news_api():

    print()
    print("START NEWS_A")

    time.sleep(4)

    print("FINISH NEWS_A")


# ============================================================
# EVENT EXECUTOR
# ============================================================

def execute_event(event):

    event_name = event["event"]
    profile = event["profile"]

    print()
    print("--------------------------------")
    print("Executing:", event_name)
    print("Profile:", profile)
    print("--------------------------------")

    if event_name == "stocks":

        fake_stocks_api()

    elif event_name == "weather":

        fake_weather_api()

    elif event_name == "news":

        fake_news_api()

    else:

        print("Unknown event:", event_name)


# ============================================================
# FAKE CLOCK
# ============================================================

# We will pretend the Sender starts at:
#
# Monday 8:59 AM
#
# Each loop advances the fake clock by one minute.
#
# This lets us test the scheduler without waiting
# for real clock time.

fake_hour = 8
fake_minute = 59


def get_fake_time():

    return (
        2026,
        9,
        28,
        fake_hour,
        fake_minute,
        0,
        Scheduler.MONDAY,
        0
    )


def advance_fake_time():

    global fake_hour
    global fake_minute

    fake_minute += 1

    if fake_minute >= 60:

        fake_minute = 0
        fake_hour += 1


# ============================================================
# MAIN TEST LOOP
# ============================================================

print()
print("================================")
print("CONTINUOUS SCHEDULER TEST")
print("================================")

print()
print("Starting fake time:")
print("Monday 8:59 AM")


for loop_number in range(6):

    current_time = get_fake_time()

    print()
    print("================================")
    print(
        "Scheduler check:",
        "{:02d}:{:02d}".format(
            current_time[3],
            current_time[4]
        )
    )
    print("================================")

    events = scheduler.check(
        current_time
    )

    if events:

        print()
        print("Events queued:")

        for event in events:

            print(
                " ",
                event["event"],
                event["profile"]
            )

        print()
        print("Beginning sequential execution...")

        for event in events:

            execute_event(event)

        print()
        print("All queued events finished.")

    else:

        print("No events due.")


    # Move fake clock forward.
    #
    # Notice that the fake clock advances only
    # after the API work finishes.
    #
    # This simulates the Sender being busy while
    # API calls are running.

    advance_fake_time()


# ============================================================
# FINISHED
# ============================================================

print()
print("================================")
print("CONTINUOUS TEST COMPLETE")
print("================================")
