# scheduler_test.py
#
# Dazzling2-mini_2
# Scheduler testing
#
# Sender Pico
#
# No API calls are made.
# No Wi-Fi is used.


from scheduler import Scheduler


scheduler = Scheduler()


# ============================================================
# BUILD TEST SCHEDULE
# ============================================================

# Monday
scheduler.add_weekly_event(
    Scheduler.MONDAY,
    7,
    0,
    "weather",
    "WEATHER_A"
)

scheduler.add_weekly_event(
    Scheduler.MONDAY,
    7,
    0,
    "news",
    "NEWS_A"
)

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
    "WEATHER_B"
)

scheduler.add_weekly_event(
    Scheduler.MONDAY,
    9,
    2,
    "news",
    "NEWS_C"
)

scheduler.add_weekly_event(
    Scheduler.MONDAY,
    12,
    0,
    "weather",
    "WEATHER_A"
)


# ============================================================
# HELPER
# ============================================================

def show_events(label, events):

    print()
    print(label)

    if not events:

        print("  No events")

        return

    for event in events:

        print(
            " ",
            event["event"],
            event["profile"]
        )


# ============================================================
# TEST 1
# ============================================================

print()
print("================================")
print("TEST 1 - Exact scheduled minute")
print("================================")

# Monday 6:59 AM
events = scheduler.check(
    (2026, 9, 28, 6, 59, 0, 0, 0)
)

show_events(
    "Monday 6:59 AM:",
    events
)


# ============================================================
# TEST 2
# ============================================================

print()
print("================================")
print("TEST 2 - Multiple events same minute")
print("================================")

# Monday 7:00 AM
events = scheduler.check(
    (2026, 9, 28, 7, 0, 0, 0, 0)
)

show_events(
    "Monday 7:00 AM:",
    events
)


# ============================================================
# TEST 3
# ============================================================

print()
print("================================")
print("TEST 3 - Missed scheduled minutes")
print("================================")

# We intentionally jump from 7:00 to 9:03.
#
# The scheduler should catch:
#
# 9:00 STOCKS_A
# 9:01 WEATHER_B
# 9:02 NEWS_C
#
# even though check() was never called during
# those exact minutes.

events = scheduler.check(
    (2026, 9, 28, 9, 3, 0, 0, 0)
)

show_events(
    "Monday 9:03 AM after missing 9:00-9:02:",
    events
)


# ============================================================
# TEST 4
# ============================================================

print()
print("================================")
print("TEST 4 - Duplicate protection")
print("================================")

# Checking 9:03 again should NOT return the
# previously executed events.

events = scheduler.check(
    (2026, 9, 28, 9, 3, 30, 0, 0)
)

show_events(
    "Monday 9:03 AM checked again:",
    events
)


# ============================================================
# TEST 5
# ============================================================

print()
print("================================")
print("TEST 5 - Later scheduled event")
print("================================")

# Jump from 9:03 to 12:02.
#
# The scheduler should catch the 12:00 event.

events = scheduler.check(
    (2026, 9, 28, 12, 2, 0, 0, 0)
)

show_events(
    "Monday 12:02 PM:",
    events
)


# ============================================================
# TEST 6
# ============================================================

print()
print("================================")
print("TEST 6 - No scheduled event")
print("================================")

events = scheduler.check(
    (2026, 9, 28, 13, 0, 0, 0, 0)
)

show_events(
    "Monday 1:00 PM:",
    events
)


# ============================================================
# TEST 7
# ============================================================

print()
print("================================")
print("TEST 7 - Special date")
print("================================")

special_scheduler = Scheduler()

special_scheduler.add_weekly_event(
    Scheduler.THURSDAY,
    9,
    0,
    "stocks",
    "STOCKS_B"
)

special_scheduler.add_special_date_event(
    "2026-12-25",
    9,
    0,
    "news",
    "HOLIDAY_NEWS"
)

special_scheduler.add_special_date_event(
    "2026-12-25",
    12,
    0,
    "weather",
    "HOLIDAY_WEATHER"
)

# Thursday December 24
events = special_scheduler.check(
    (2026, 12, 24, 9, 0, 0, 3, 0)
)

show_events(
    "Thursday December 24, 9:00 AM:",
    events
)


# Move into the special date.
events = special_scheduler.check(
    (2026, 12, 25, 9, 1, 0, 4, 0)
)

show_events(
    "Friday December 25, after missing 9:00 AM:",
    events
)


# ============================================================
# FINISHED
# ============================================================

print()
print("================================")
print("SCHEDULER TEST COMPLETE")
print("================================")from scheduler import Scheduler


# -------------------------------------------------
# Create Scheduler
# -------------------------------------------------

scheduler = Scheduler()


# -------------------------------------------------
# Normal Weekly Schedule
# -------------------------------------------------

# Thursday 09:00
scheduler.add_weekly_event(
    Scheduler.THURSDAY,
    9,
    0,
    "stocks",
    "STOCKS_B"
)

# Thursday 12:00
scheduler.add_weekly_event(
    Scheduler.THURSDAY,
    12,
    0,
    "weather",
    "WEATHER_B"
)


# -------------------------------------------------
# Special Date Schedule
# -------------------------------------------------

# Christmas Day
scheduler.add_special_date_event(
    "2026-12-25",
    9,
    0,
    "news",
    "HOLIDAY_NEWS"
)

scheduler.add_special_date_event(
    "2026-12-25",
    12,
    0,
    "weather",
    "HOLIDAY_WEATHER"
)


# -------------------------------------------------
# Test Helper
# -------------------------------------------------

def run_test(label, test_time):

    print(label)

    events = scheduler.check(test_time)

    if events:

        for event in events:

            print(
                "  EVENT:",
                event["event"],
                "| PROFILE:",
                event["profile"]
            )

    else:

        print("  No events")

    print("")


# -------------------------------------------------
# Normal Thursday
# -------------------------------------------------

print("")
print("==============================")
print("NORMAL THURSDAY")
print("==============================")
print("")

run_test(
    "Thursday 09:00",
    (2026, 12, 24, 9, 0, 0, 3, 0)
)

run_test(
    "Thursday 12:00",
    (2026, 12, 24, 12, 0, 0, 3, 0)
)


# -------------------------------------------------
# Special Date
# -------------------------------------------------

print("==============================")
print("SPECIAL DATE OVERRIDE")
print("==============================")
print("")

run_test(
    "Friday 09:00 - Christmas Day",
    (2026, 12, 25, 9, 0, 0, 4, 0)
)

run_test(
    "Friday 12:00 - Christmas Day",
    (2026, 12, 25, 12, 0, 0, 4, 0)
)


# -------------------------------------------------
# Verify Normal Thursday Events Do NOT Run
# -------------------------------------------------

print("==============================")
print("SPECIAL DATE REPLACEMENT TEST")
print("==============================")
print("")

run_test(
    "Christmas Day 09:00 should NOT be STOCKS_B",
    (2026, 12, 25, 9, 0, 0, 4, 0)
)

run_test(
    "Christmas Day 12:00 should NOT be WEATHER_B",
    (2026, 12, 25, 12, 0, 0, 4, 0)
)


print("==============================")
print("TEST COMPLETE")
print("==============================")
