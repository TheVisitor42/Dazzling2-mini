# event_executor.py
#
# Dazzling2-mini_2
# Sender Pico
#
# Receives scheduled events and runs
# the appropriate task.
#
# Weather is now connected to the
# WeatherTask module.
#
# Other tasks remain fake for now.


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

        return True


    def stocks_b(self):

        print()
        print("START STOCKS_B")

        print("  Getting index data...")

        time.sleep(2)

        print("  Processing index data...")

        time.sleep(1)

        print("  STOCKS_B complete")

        return True


    def stocks_c(self):

        print()
        print("START STOCKS_C")

        print("  Getting random stock...")

        time.sleep(2)

        print("  Processing stock data...")

        time.sleep(1)

        print("  STOCKS_C complete")

        return True


    # ========================================================
    # WEATHER TASKS
    # ========================================================

    def weather_a(self):

        print()
        print("START WEATHER_A")

        result = self.weather_task.run()

        if result["success"]:

            print("  WEATHER_A successful")

        else:

            print("  WEATHER_A FAILED")
            print("  Error:", result["error"])

        return result


    def weather_b(self):

        print()
        print("START WEATHER_B")

        print("  Getting 7-day forecast...")

        time.sleep(2)

        print("  Processing forecast data...")

        time.sleep(1)

        print("  WEATHER_B complete")

        return True


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

        return True


    def news_b(self):

        print()
        print("START NEWS_B")

        print("  Getting local news...")

        time.sleep(2)

        print("  Processing local news...")

        time.sleep(1)

        print("  NEWS_B complete")

        return True


    def news_c(self):

        print()
        print("START NEWS_C")

        print("  Getting sports news...")

        time.sleep(2)

        print("  Processing sports data...")

        time.sleep(1)

        print("  NEWS_C complete")

        return True


    # ========================================================
    # CLOCK TASK
    # ========================================================

    def clock(self):

        print()
        print("START CLOCK")

        print("  Simulating NTP synchronization...")

        time.sleep(2)

        print("  CLOCK synchronization complete")

        return True


    # ========================================================
    # EXECUTE EVENT
    # ========================================================

    def execute(self, event):

        event_name = event["event"]
        profile = event["profile"]

        print()
        print("================================")
        print("EXECUTING EVENT")
        print("================================")

        print("Event:", event_name)
        print("Profile:", profile)

        self.event_count += 1

        # ----------------------------------------------------
        # STOCKS
        # ----------------------------------------------------

        if event_name == "stocks":

            if profile == "STOCKS_A":

                return self.stocks_a()

            elif profile == "STOCKS_B":

                return self.stocks_b()

            elif profile == "STOCKS_C":

                return self.stocks_c()

            else:

                print(
                    "Unknown stocks profile:",
                    profile
                )

                return False


        # ----------------------------------------------------
        # WEATHER
        # ----------------------------------------------------

        elif event_name == "weather":

            if profile == "WEATHER_A":

                return self.weather_a()

            elif profile == "WEATHER_B":

                return self.weather_b()

            else:

                print(
                    "Unknown weather profile:",
                    profile
                )

                return False


        # ----------------------------------------------------
        # NEWS
        # ----------------------------------------------------

        elif event_name == "news":

            if profile == "NEWS_A":

                return self.news_a()

            elif profile == "NEWS_B":

                return self.news_b()

            elif profile == "NEWS_C":

                return self.news_c()

            else:

                print(
                    "Unknown news profile:",
                    profile
                )

                return False


        # ----------------------------------------------------
        # CLOCK
        # ----------------------------------------------------

        elif event_name == "clock":

            if profile == "CLOCK":

                return self.clock()

            else:

                print(
                    "Unknown clock profile:",
                    profile
                )

                return False


        # ----------------------------------------------------
        # UNKNOWN EVENT
        # ----------------------------------------------------

        else:

            print(
                "Unknown event type:",
                event_name
            )

            return False
