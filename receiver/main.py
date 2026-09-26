from machine import UART, Pin
import time

from oled import (
    initialize_oleds,
    display_text,
    start_news,
    update_news
)


# =================================================
# TEST SCHEDULE
# =================================================

WEATHER_INTERVAL = 60       # 1 minute
STOCKS_INTERVAL = 30        # 30 seconds
NEWS_INTERVAL = 120         # 2 minutes
CLOCK_INTERVAL = 1          # 1 second


# =================================================
# UART
# =================================================

uart = UART(
    0,
    baudrate=115200,
    tx=Pin(0),
    rx=Pin(1)
)


# =================================================
# Initialize OLEDs
# =================================================

print("Starting OLEDs...")

initialize_oleds()

print("OLEDs initialized.")


# =================================================
# Test Data
# =================================================

weather_counter = 0
stocks_counter = 0
news_counter = 0

current_news_stories = []


# =================================================
# Timers
# =================================================

last_weather_update = time.ticks_ms()
last_stocks_update = time.ticks_ms()
last_news_update = time.ticks_ms()
last_clock_update = time.ticks_ms()


# =================================================
# TEST WEATHER
# =================================================

def update_weather():

    global weather_counter

    weather_counter += 1

    temperature = 70 + weather_counter
    wind = 5 + weather_counter
    rain = weather_counter % 4

    display_text(
        0,
        "WEATHER",
        "TEMP " + str(temperature),
        "WIND " + str(wind),
        "RAIN " + str(rain)
    )

    print(
        "Weather update:",
        weather_counter
    )


# =================================================
# TEST STOCKS
# =================================================

def update_stocks():

    global stocks_counter

    stocks_counter += 1

    brk_price = 500 + stocks_counter
    ntdoy_price = 20 + stocks_counter

    display_text(
        1,
        "STOCKS",
        "BRK.B $" + str(brk_price),
        "NTDOY $" + str(ntdoy_price),
        "UPDATE " + str(stocks_counter)
    )

    print(
        "Stocks update:",
        stocks_counter
    )


# =================================================
# TEST NEWS
# =================================================

def update_news_data():

    global news_counter
    global current_news_stories

    news_counter += 1

    stories = [
        "Test news update number " + str(news_counter) +
        " is now being displayed on the news screen.",

        "Dazzling2 mini scheduler test is running successfully.",

        "News pages continue cycling while other OLEDs update.",

        "This is test data and does not use any API calls."
    ]

    current_news_stories = stories

    start_news(stories)

    print(
        "News update:",
        news_counter
    )


# =================================================
# TEST CLOCK
# =================================================

def update_clock():

    current_time = time.localtime()

    hour = current_time[3]
    minute = current_time[4]
    second = current_time[5]

    time_string = "{:02d}:{:02d}:{:02d}".format(
        hour,
        minute,
        second
    )

    display_text(
        3,
        "CLOCK",
        time_string
    )


# =================================================
# Main Scheduler
# =================================================

print("Starting test scheduler...")

# Force all displays to update immediately
update_weather()
update_stocks()
update_news_data()
update_clock()


while True:

    now = time.ticks_ms()


    # ---------------------------------------------
    # Weather
    # ---------------------------------------------

    if time.ticks_diff(
        now,
        last_weather_update
    ) >= WEATHER_INTERVAL * 1000:

        last_weather_update = now

        update_weather()


    # ---------------------------------------------
    # Stocks
    # ---------------------------------------------

    if time.ticks_diff(
        now,
        last_stocks_update
    ) >= STOCKS_INTERVAL * 1000:

        last_stocks_update = now

        update_stocks()


    # ---------------------------------------------
    # News
    # ---------------------------------------------

    if time.ticks_diff(
        now,
        last_news_update
    ) >= NEWS_INTERVAL * 1000:

        last_news_update = now

        update_news_data()


    # ---------------------------------------------
    # Clock
    # ---------------------------------------------

    if time.ticks_diff(
        now,
        last_clock_update
    ) >= CLOCK_INTERVAL * 1000:

        last_clock_update = now

        update_clock()


    # ---------------------------------------------
    # News Paging
    # ---------------------------------------------

    update_news()


    # ---------------------------------------------
    # Small Scheduler Delay
    # ---------------------------------------------

    time.sleep_ms(10)
