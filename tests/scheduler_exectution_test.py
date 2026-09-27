# scheduler_execution_test.py
#
# Dazzling2-mini_2
# Sender Pico
#
# Tests:
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


# Three events close together.
#
# STOCKS_A  -> 9:00
# WEATHER_A -> 9:01
# NEWS_A    -> 9:02

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

    print("  Simulating stocks API call...")

    time.sleep(3)

    print("FINISH STOCKS_A")


def fake_weather_api():

    print()
    print("START WEATHER_A")

    print("  Simulating weather API call...")

    time.sleep(2)

    print("FINISH WEATHER_A")


def fake_news_api():

    print()
    print("START NEWS_A")

    print("  Simulating news API call...")

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
    print("Executing:")
    print("Event:", event_name)
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
# SIMULATE TIME
# ============================================================

print()
print("================================")
print("SCHEDULER EXECUTION TEST")
print("================================")

print()
print("Initial scheduler check:")
print("Monday 8:59 AM")

events = scheduler.check(
    (2026, 9, 28, 8, 59, 0, 0, 0)
)

print("Events returned:", events)


# ============================================================
# JUMP TO 9:03
# ============================================================

print()
print("================================")
print("Jumping to 9:03 AM")
print("================================")

print()
print("Scheduler should return:")
print("1. STOCKS_A")
print("2. WEATHER_A")
print("3. NEWS_A")

events = scheduler.check(
    (2026, 9, 28, 9, 3, 0, 0, 0)
)


print()
print("Events returned:")
print(events)


# ============================================================
# EXECUTE QUEUE
# ============================================================

print()
print("================================")
print("EXECUTING EVENT QUEUE")
print("================================")


for event in events:

    execute_event(event)


# ============================================================
# FINISHED
# ============================================================

print()
print("================================")
print("EXECUTION TEST COMPLETE")
print("================================")
