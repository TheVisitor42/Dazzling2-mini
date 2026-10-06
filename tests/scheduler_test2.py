# scheduler_test.py
#
# Dazzling2-mini_2
# Weekly Scheduler Test
#
# This test:
# - Builds the complete weekly schedule
# - Tests every scheduled time Monday-Sunday
# - Uses fake times
# - Does NOT use Wi-Fi
# - Does NOT call any APIs
# - Does NOT execute events
#
# It only tests whether the Scheduler returns
# the correct events at the correct times.


from scheduler import Scheduler


# ============================================
# BUILD WEEKLY SCHEDULE
# ============================================

def build_scheduler():

    scheduler = Scheduler()

    # --------------------------------------------
    # MONDAY
    # --------------------------------------------

    scheduler.add_weekly_event(
        Scheduler.MONDAY,
        6, 59,
        "clock",
        "CLOCK"
    )

    scheduler.add_weekly_event(
        Scheduler.MONDAY,
        7, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.MONDAY,
        7, 0,
        "news",
        "NEWS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.MONDAY,
        9, 0,
        "stocks",
        "STOCKS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.MONDAY,
        12, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.MONDAY,
        16, 0,
        "stocks",
        "STOCKS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.MONDAY,
        18, 0,
        "weather",
        "WEATHER_B"
    )

    scheduler.add_weekly_event(
        Scheduler.MONDAY,
        18, 0,
        "stocks",
        "STOCKS_B"
    )


    # --------------------------------------------
    # TUESDAY
    # --------------------------------------------

    scheduler.add_weekly_event(
        Scheduler.TUESDAY,
        6, 59,
        "clock",
        "CLOCK"
    )

    scheduler.add_weekly_event(
        Scheduler.TUESDAY,
        7, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.TUESDAY,
        7, 0,
        "news",
        "NEWS_B"
    )

    scheduler.add_weekly_event(
        Scheduler.TUESDAY,
        9, 0,
        "stocks",
        "STOCKS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.TUESDAY,
        12, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.TUESDAY,
        16, 0,
        "stocks",
        "STOCKS_A"
    )


    # --------------------------------------------
    # WEDNESDAY
    # --------------------------------------------

    scheduler.add_weekly_event(
        Scheduler.WEDNESDAY,
        6, 59,
        "clock",
        "CLOCK"
    )

    scheduler.add_weekly_event(
        Scheduler.WEDNESDAY,
        7, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.WEDNESDAY,
        7, 0,
        "news",
        "NEWS_B"
    )

    scheduler.add_weekly_event(
        Scheduler.WEDNESDAY,
        9, 0,
        "stocks",
        "STOCKS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.WEDNESDAY,
        9, 0,
        "weather",
        "WEATHER_B"
    )

    scheduler.add_weekly_event(
        Scheduler.WEDNESDAY,
        12, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.WEDNESDAY,
        16, 0,
        "stocks",
        "STOCKS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.WEDNESDAY,
        16, 0,
        "news",
        "NEWS_C"
    )

    scheduler.add_weekly_event(
        Scheduler.WEDNESDAY,
        18, 0,
        "news",
        "NEWS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.WEDNESDAY,
        18, 0,
        "stocks",
        "STOCKS_C"
    )


    # --------------------------------------------
    # THURSDAY
    # --------------------------------------------

    scheduler.add_weekly_event(
        Scheduler.THURSDAY,
        6, 59,
        "clock",
        "CLOCK"
    )

    scheduler.add_weekly_event(
        Scheduler.THURSDAY,
        7, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.THURSDAY,
        7, 0,
        "news",
        "NEWS_B"
    )

    scheduler.add_weekly_event(
        Scheduler.THURSDAY,
        9, 0,
        "stocks",
        "STOCKS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.THURSDAY,
        12, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.THURSDAY,
        16, 0,
        "stocks",
        "STOCKS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.THURSDAY,
        16, 0,
        "news",
        "NEWS_C"
    )

    scheduler.add_weekly_event(
        Scheduler.THURSDAY,
        18, 0,
        "news",
        "NEWS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.THURSDAY,
        18, 0,
        "weather",
        "WEATHER_A"
    )


    # --------------------------------------------
    # FRIDAY
    # --------------------------------------------

    scheduler.add_weekly_event(
        Scheduler.FRIDAY,
        6, 59,
        "clock",
        "CLOCK"
    )

    scheduler.add_weekly_event(
        Scheduler.FRIDAY,
        7, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.FRIDAY,
        9, 0,
        "stocks",
        "STOCKS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.FRIDAY,
        12, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.FRIDAY,
        12, 0,
        "news",
        "NEWS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.FRIDAY,
        16, 0,
        "stocks",
        "STOCKS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.FRIDAY,
        18, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.FRIDAY,
        18, 0,
        "stocks",
        "STOCKS_B"
    )


    # --------------------------------------------
    # SATURDAY
    # --------------------------------------------

    scheduler.add_weekly_event(
        Scheduler.SATURDAY,
        6, 59,
        "clock",
        "CLOCK"
    )

    scheduler.add_weekly_event(
        Scheduler.SATURDAY,
        7, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.SATURDAY,
        7, 0,
        "news",
        "NEWS_B"
    )

    scheduler.add_weekly_event(
        Scheduler.SATURDAY,
        12, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.SATURDAY,
        12, 0,
        "news",
        "NEWS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.SATURDAY,
        19, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.SATURDAY,
        19, 0,
        "news",
        "NEWS_C"
    )


    # --------------------------------------------
    # SUNDAY
    # --------------------------------------------

    scheduler.add_weekly_event(
        Scheduler.SUNDAY,
        6, 59,
        "clock",
        "CLOCK"
    )

    scheduler.add_weekly_event(
        Scheduler.SUNDAY,
        7, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.SUNDAY,
        7, 0,
        "news",
        "NEWS_A"
    )

    scheduler.add_weekly_event(
        Scheduler.SUNDAY,
        11, 0,
        "weather",
        "WEATHER_B"
    )

    scheduler.add_weekly_event(
        Scheduler.SUNDAY,
        11, 0,
        "news",
        "NEWS_B"
    )

    scheduler.add_weekly_event(
        Scheduler.SUNDAY,
        15, 0,
        "weather",
        "WEATHER_A"
    )

    scheduler.add_weekly_event(
        Scheduler.SUNDAY,
        22, 0,
        "news",
        "NEWS_C"
    )

    return scheduler


# ============================================
# FAKE TIME
# ============================================

def fake_time(
    weekday,
    hour,
    minute
):

    # October 5, 2026 is Monday.
    #
    # Monday    = 5
    # Tuesday   = 6
    # Wednesday = 7
    # Thursday  = 8
    # Friday    = 9
    # Saturday  = 10
    # Sunday    = 11

    day = 5 + weekday

    return (
        2026,
        10,
        day,
        hour,
        minute,
        0,
        weekday,
        0
    )


# ============================================
# PRINT EVENTS
# ============================================

def print_events(
    day_name,
    hour,
    minute,
    events
):

    print()
    print("--------------------------------")

    print(
        "{} {:02d}:{:02d}".format(
            day_name.upper(),
            hour,
            minute
        )
    )

    print("--------------------------------")

    if not events:

        print("NO EVENTS")

        return

    for event in events:

        print(
            event["event"],
            "/",
            event["profile"]
        )


# ============================================
# TEST ONE DAY
# ============================================

def test_day(
    weekday,
    day_name,
    test_times
):

    print()
    print()
    print("================================")
    print("TESTING", day_name.upper())
    print("================================")

    # Fresh scheduler for each day.
    scheduler = build_scheduler()

    for hour, minute in test_times:

        events = scheduler.check(
            fake_time(
                weekday,
                hour,
                minute
            )
        )

        print_events(
            day_name,
            hour,
            minute,
            events
        )


# ============================================
# RUN TEST
# ============================================

print()
print("================================")
print("Dazzling2-mini_2 WEEKLY SCHEDULE TEST")
print("================================")


# --------------------------------------------
# MONDAY
# --------------------------------------------

test_day(
    Scheduler.MONDAY,
    "Monday",
    [
        (6, 59),
        (7, 0),
        (9, 0),
        (12, 0),
        (16, 0),
        (18, 0)
    ]
)


# --------------------------------------------
# TUESDAY
# --------------------------------------------

test_day(
    Scheduler.TUESDAY,
    "Tuesday",
    [
        (6, 59),
        (7, 0),
        (9, 0),
        (12, 0),
        (16, 0)
    ]
)


# --------------------------------------------
# WEDNESDAY
# --------------------------------------------

test_day(
    Scheduler.WEDNESDAY,
    "Wednesday",
    [
        (6, 59),
        (7, 0),
        (9, 0),
        (12, 0),
        (16, 0),
        (18, 0)
    ]
)


# --------------------------------------------
# THURSDAY
# --------------------------------------------

test_day(
    Scheduler.THURSDAY,
    "Thursday",
    [
        (6, 59),
        (7, 0),
        (9, 0),
        (12, 0),
        (16, 0),
        (18, 0)
    ]
)


# --------------------------------------------
# FRIDAY
# --------------------------------------------

test_day(
    Scheduler.FRIDAY,
    "Friday",
    [
        (6, 59),
        (7, 0),
        (9, 0),
        (12, 0),
        (16, 0),
        (18, 0)
    ]
)


# --------------------------------------------
# SATURDAY
# --------------------------------------------

test_day(
    Scheduler.SATURDAY,
    "Saturday",
    [
        (6, 59),
        (7, 0),
        (12, 0),
        (19, 0)
    ]
)


# --------------------------------------------
# SUNDAY
# --------------------------------------------

test_day(
    Scheduler.SUNDAY,
    "Sunday",
    [
        (6, 59),
        (7, 0),
        (11, 0),
        (15, 0),
        (22, 0)
    ]
)


# ============================================
# COMPLETE
# ============================================

print()
print("================================")
print("WEEKLY SCHEDULE TEST COMPLETE")
print("================================")

