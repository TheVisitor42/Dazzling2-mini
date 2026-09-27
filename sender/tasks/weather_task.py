# weather_task.py
#
# Dazzling2-mini_2
# Sender Pico
#
# Real weather API task.
#
# Returns the common task result format:
#
# success = whether the API call worked
# update  = whether new data should be sent to Receiver
# data    = processed weather data
# error   = error description


import time
import json
import usocket


class WeatherTask:

    API_HOST = "open-weather13.p.rapidapi.com"

    API_KEY = ""

    CITY = "fort%20worth"

    def __init__(self):

        # Keep this for diagnostics/testing.
        self.last_good_data = None


    def run(self):

        print()
        print("================================")
        print("WEATHER TASK")
        print("================================")

        print("Connecting to weather API...")


        try:

            # ------------------------------------------------
            # CONNECT
            # ------------------------------------------------

            addr = usocket.getaddrinfo(
                self.API_HOST,
                443
            )[0][-1]

            sock = usocket.socket(
                usocket.AF_INET,
                usocket.SOCK_STREAM
            )

            sock.connect(addr)


            # ------------------------------------------------
            # TLS
            # ------------------------------------------------

            import ussl

            sock = ussl.wrap_socket(
                sock,
                server_hostname=self.API_HOST
            )


            # ------------------------------------------------
            # HTTP REQUEST
            # ------------------------------------------------

            request = (
                "GET /city?city={}&lang=EN HTTP/1.1\r\n"
                "Host: {}\r\n"
                "x-rapidapi-key: {}\r\n"
                "x-rapidapi-host: {}\r\n"
                "Connection: close\r\n"
                "\r\n"
            ).format(
                self.CITY,
                self.API_HOST,
                self.API_KEY,
                self.API_HOST
            )

            sock.write(request.encode())


            # ------------------------------------------------
            # RECEIVE RESPONSE
            # ------------------------------------------------

            response = b""

            while True:

                chunk = sock.read(512)

                if not chunk:
                    break

                response += chunk


            sock.close()


            # ------------------------------------------------
            # SEPARATE HTTP HEADERS FROM JSON
            # ------------------------------------------------

            header_end = response.find(b"\r\n\r\n")

            if header_end == -1:

                return {
                    "success": False,
                    "update": False,
                    "data": None,
                    "error": "Invalid HTTP response"
                }


            body = response[
                header_end + 4:
            ]


            # ------------------------------------------------
            # PARSE JSON
            # ------------------------------------------------

            weather_response = json.loads(
                body.decode("utf-8")
            )


            # ------------------------------------------------
            # CHECK API RESPONSE
            # ------------------------------------------------

            if "main" not in weather_response:

                error_message = weather_response.get(
                    "message",
                    "Unknown API error"
                )

                print(
                    "Weather API error:",
                    error_message
                )

                return {
                    "success": False,
                    "update": False,
                    "data": None,
                    "error": str(error_message)
                }


            # ------------------------------------------------
            # EXTRACT DATA
            # ------------------------------------------------

            city = weather_response.get(
                "name",
                "Unknown"
            )

            main_data = weather_response.get(
                "main",
                {}
            )

            weather_list = weather_response.get(
                "weather",
                []
            )

            wind_data = weather_response.get(
                "wind",
                {}
            )

            temperature = main_data.get(
                "temp"
            )

            feels_like = main_data.get(
                "feels_like"
            )

            humidity = main_data.get(
                "humidity"
            )

            wind_speed = wind_data.get(
                "speed"
            )

            wind_direction = wind_data.get(
                "deg"
            )

            cloud_coverage = weather_response.get(
                "clouds",
                {}
            ).get(
                "all"
            )

            if weather_list:

                description = weather_list[0].get(
                    "description",
                    "Unknown"
                )

            else:

                description = "Unknown"


            # ------------------------------------------------
            # BUILD OUR INTERNAL WEATHER DATA
            # ------------------------------------------------

            weather_data = {

                "city": city,

                "temperature": temperature,

                "feels_like": feels_like,

                "humidity": humidity,

                "wind_speed": wind_speed,

                "wind_direction": wind_direction,

                "cloud_coverage": cloud_coverage,

                "description": description
            }


            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            self.last_good_data = weather_data

            print()
            print("Weather API successful.")

            print("City:", city)
            print("Temperature:", temperature)
            print("Feels like:", feels_like)
            print("Humidity:", humidity)
            print("Wind:", wind_speed)
            print("Description:", description)

            return {

                "success": True,

                "update": True,

                "data": weather_data,

                "error": None
            }


        except Exception as error:

            print()
            print("Weather API FAILED.")
            print("Error:", error)

            return {

                "success": False,

                "update": False,

                "data": None,

                "error": str(error)
            }
