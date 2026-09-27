from scheduler import Scheduler


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
