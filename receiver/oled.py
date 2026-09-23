import time
import ssd1306
from multiplexer import i2c, select_mux_channel

OLED_ADDR = 0x3C
WIDTH = 128
HEIGHT = 64

oleds = {}


def initialize_oleds():

    for ch in range(4):

        select_mux_channel(ch)

        oled = ssd1306.SSD1306_I2C(
            WIDTH,
            HEIGHT,
            i2c,
            addr=OLED_ADDR
        )

        oled.fill(0)
        oled.text("OLED #{}".format(ch), 0, 0)
        oled.show()

        oleds[ch] = oled

        time.sleep_ms(200)

    select_mux_channel(255)


def display_text(display_num, line1="", line2="", line3="", line4=""):

    oled = oleds[display_num]

    select_mux_channel(display_num)

    oled.fill(0)

    oled.text(line1, 0, 0)
    oled.text(line2, 0, 16)
    oled.text(line3, 0, 32)
    oled.text(line4, 0, 48)

    oled.show()

    select_mux_channel(255)
