# scheduler_executor_integration_test.py
#
# Dazzling2-mini_2
# Sender Pico
#
# Tests:
# scheduler.py + event_executor.py
#
# NO real APIs
# NO Wi-Fi
# NO UART


from scheduler import Scheduler
from event_executor import EventExecutor
import time


# ============================================================
# CREATE SCHEDULER
# ============================================================

scheduler = Scheduler()


# Three events close together.

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
# CREATE EXECUTOR
# ============================================================

executor = EventExecutor()


# ============================================================
# FAKE CLOCK
# ============================================================

fake_time = (
    2026,
    9,
    28,
    8,
    59,
    0,
    Scheduler.MONDAY,
    0
)


def set_fake_time(hour, minute):

    global fake_time

    fake_time = (
        2026,
        9,
        28,
        hour,
        minute,
        0,
        Scheduler.MONDAY,
        0
    )


def get_fake_time():

    return fake_time


# ============================================================
# CHECK SCHEDULER AND EXECUTE EVENTS
# ============================================================

def check_and_execute():

    current_time = get_fake_time()

    print()
    print("================================")
    print(
        "SCHEDULER CHECK {:02d}:{:02d}".format(
            current_time[3],
            current_time[4]
        )
    )
    print("================================")

    events = scheduler.check(
        current_time
    )

    if not events:

        print("No events due.")

        return


    print()
    print("Events returned by scheduler:")

    for event in events:

        print(
            " ",
            event["event"],
            event["profile"]
        )


    print()
    print("Passing events to executor...")


    for event in events:

        result = executor.execute(
            event
        )

        print(
            "Execution result:",
            result
        )


# ============================================================
# TEST START
# ============================================================

print()
print("================================")
print("SCHEDULER + EXECUTOR TEST")
print("================================")


# ============================================================
# STEP 1
# ============================================================

print()
print("STEP 1")
print("Starting at 8:59 AM")

set_fake_time(8, 59)

check_and_execute()


# ============================================================
# STEP 2
# ============================================================

print()
print("STEP 2")
print("Moving to 9:00 AM")

set_fake_time(9, 0)

check_and_execute()


# ============================================================
# STEP 3
# ============================================================

print()
print("STEP 3")
print()
print("STOCKS_A has just finished.")
print()
print("While it was running:")
print()
print("9:01 -> WEATHER_A became due")
print("9:02 -> NEWS_A became due")
print()
print("Now moving directly to 9:03.")


set_fake_time(9, 3)

check_and_execute()


# ============================================================
# STEP 4
# ============================================================

print()
print("STEP 4")
print("Checking 9:03 again.")
print()
print("Nothing should execute twice.")

check_and_execute()


# ============================================================
# SUMMARY
# ============================================================

print()
print("================================")
print("INTEGRAT
