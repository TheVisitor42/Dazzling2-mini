from machine import SPI, Pin
import time


class W25Q64:

    # Commands
    WRITE_ENABLE = 0x06
    READ_STATUS = 0x05
    PAGE_PROGRAM = 0x02
    READ_DATA = 0x03
    SECTOR_ERASE = 0x20

    # W25Q64 parameters
    PAGE_SIZE = 256
    SECTOR_SIZE = 4096

    def __init__(self):
        self.spi = SPI(
            1,
            baudrate=10_000_000,
            polarity=0,
            phase=0,
            sck=Pin(14),
            mosi=Pin(11),
            miso=Pin(12)
        )

        self.cs = Pin(13, Pin.OUT)
        self.cs.value(1)

    def _select(self):
        self.cs.value(0)

    def _deselect(self):
        self.cs.value(1)

    def read_jedec_id(self):
        self._select()

        self.spi.write(b'\x9F')
        data = self.spi.read(3)

        self._deselect()

        return data

    def read_status(self):
        self._select()

        self.spi.write(bytes([self.READ_STATUS]))
        status = self.spi.read(1)[0]

        self._deselect()

        return status

    def write_enable(self):
        self._select()

        self.spi.write(bytes([self.WRITE_ENABLE]))

        self._deselect()

    def wait_until_ready(self):
        while self.read_status() & 0x01:
            time.sleep_ms(1)

    def erase_sector(self, address):
        # Align address to beginning of sector
        address = address & ~(self.SECTOR_SIZE - 1)

        self.write_enable()

        self._select()

        self.spi.write(bytes([
            self.SECTOR_ERASE,
            (address >> 16) & 0xFF,
            (address >> 8) & 0xFF,
            address & 0xFF
        ]))

        self._deselect()

        self.wait_until_ready()

    def _write_page(self, address, data):
        """
        Write a single chunk that must fit inside one 256-byte page.
        """

        self.write_enable()

        self._select()

        self.spi.write(bytes([
            self.PAGE_PROGRAM,
            (address >> 16) & 0xFF,
            (address >> 8) & 0xFF,
            address & 0xFF
        ]))

        self.spi.write(data)

        self._deselect()

        self.wait_until_ready()

    def write(self, address, data):
        """
        Write any length of data.

        Automatically splits writes at 256-byte page boundaries.
        """

        if not isinstance(data, (bytes, bytearray)):
            raise TypeError("data must be bytes or bytearray")

        offset = 0
        remaining = len(data)

        while remaining > 0:

            page_offset = address % self.PAGE_SIZE

            space_in_page = self.PAGE_SIZE - page_offset

            chunk_size = min(remaining, space_in_page)

            chunk = data[offset:offset + chunk_size]

            self._write_page(address, chunk)

            address += chunk_size
            offset += chunk_size
            remaining -= chunk_size

    def read(self, address, length):
        """
        Read length bytes starting at address.
        """

        self._select()

        self.spi.write(bytes([
            self.READ_DATA,
            (address >> 16) & 0xFF,
            (address >> 8) & 0xFF,
            address & 0xFF
        ]))

        data = self.spi.read(length)

        self._deselect()

        return data


flash = W25Q64()
