# event_executor.py
#
# Dazzling2-mini_2
# Sender Pico
#
# Receives scheduled events and runs
# the appropriate task.
#
# A successful task can provide an update.
# A failed task does not provide an update.
#
# UART is NOT handled here yet.


import time

from tasks.weather_task import WeatherTask


class EventExecutor:

    def __init__(self):

        self.event_count = 0

        # Weather task
        self.weather_task = WeatherTask()


    # ========================================================
    # FAKE STOCKS TASKS
    # ========================================================

    def stocks_a(self):

        print()
        print("START STOCKS_A")

        print("  Getting main portfolio data...")

        time.sleep(2)

        print("  Processing stock data...")

        time.sleep(1)

        print("  STOCKS_A complete")

        return {
            "success": True,
            "update": True,
            "data": None,
            "error": None
        }


    def stocks_b(self):

        print()
        print("START STOCKS_B")

        print("  Getting index data...")

        time.sleep(2)

        print("  Processing index data...")

        time.sleep(1)

        print("  STOCKS_B complete")

        return {
            "success": True,
            "update": True,
            "data": None,
            "error": None
        }


    def stocks_c(self):

        print()
        print("START STOCKS_C")

        print("  Getting random stock...")

        time.sleep(2)

        print("  Processing stock data...")

        time.sleep(1)

        print("  STOCKS_C complete")

        return {
            "success": True,
            "update": True,
            "data": None,
            "error": None
        }


    # ========================================================
    # WEATHER TASKS
    # ========================================================

    def weather_a(self):

        print()
        print("START WEATHER_A")

        result = self.weather_task.run()

        if result["success"]:

            print("  WEATHER_A successful")
            print("  New weather data available")

            return {
                "success": True,
                "update": True,
                "data": result["data"],
                "error": None
            }

        else:

            print("  WEATHER_A FAILED")
            print("  Error:", result["error"])
            print("  No update will be sent")

            return {
                "success": False,
                "update": False,
                "data": None,
                "error": result["error"]
            }


    def weather_b(self):

        print()
        print("START WEATHER_B")

        print("  Getting 7-day forecast...")

        time.sleep(2)

        print("  Processing forecast data...")

        time.sleep(1)

        print("  WEATHER_B complete")

        return {
            "success": True,
            "update": True,
            "data": None,
            "error": None
        }


    # ========================================================
    # FAKE NEWS TASKS
    # ========================================================

    def news_a(self):

        print()
        print("START NEWS_A")

        print("  Getting top headlines...")

        time.sleep(2)

        print("  Processing headlines...")

        time.sleep(1)

        print("  NEWS_A complete")

        return {
            "success": True,
            "update": True,
            "data": None,
            "error": None
        }


    def news_b(self):

        print()
        print("START NEWS_B")

        print("  Getting local news...")

        time.sleep(2)

        print("  Processing local news...")

        time.sleep(1)

        print("  NEWS_B complete")

        return {
            "success": True,
            "update": True,
            "data": None,
            "error": None
        }


    def news_c(self):

        print()
        print("START 
