from machine import I2C, Pin
import time


i2c = I2C(
    1,
    scl=Pin(3),
    sda=Pin(2),
    freq=400000
)


TCA_ADDR = 0x70


def select_mux_channel(channel):

    if channel > 3:

        i2c.writeto(
            TCA_ADDR,
            bytes([0])
        )

    else:

        i2c.writeto(
            TCA_ADDR,
            bytes([1 << channel])
        )

    time.sleep_ms(1)
