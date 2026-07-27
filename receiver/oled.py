#OLED setup 

#address_oled12864 = "0xC3"

#---

from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from luma.core.render import canvas


# -----------------------------------------
# OLED Initialization
# -----------------------------------------

serial = i2c(
    port=1,
    address=0x3C
)

oled = ssd1306(serial)


# -----------------------------------------
# Display Functions
# -----------------------------------------

def display_weather(packet):

    weather = packet["data"]

    with canvas(oled) as draw:

        draw.text(
            (0, 0),
            "WEATHER",
            fill="white"
        )

        draw.text(
            (0, 15),
            "Temp: {} F".format(
                weather["temperature"]
            ),
            fill="white"
        )

        draw.text(
            (0, 30),
            "Wind: {} mph".format(
                weather["wind_speed"]
            ),
            fill="white"
        )

        draw.text(
            (0, 45),
            "Rain: {}".format(
                weather["precipitation"]
            ),
            fill="white"
        )
