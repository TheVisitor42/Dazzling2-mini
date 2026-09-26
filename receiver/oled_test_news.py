import time
import ssd1306

from multiplexer import i2c, select_mux_channel


OLED_ADDR = 0x3C
WIDTH = 128
HEIGHT = 64

NEWS_DISPLAY = 2

# -------------------------------------------------
# OLED Storage
# -------------------------------------------------

oleds = {}


# -------------------------------------------------
# OLED Initialization
# -------------------------------------------------

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


# -------------------------------------------------
# Generic OLED Display
# -------------------------------------------------

def display_text(
    display_num,
    line1="",
    line2="",
    line3="",
    line4="",
    line5=""
):

    oled = oleds[display_num]

    select_mux_channel(display_num)

    oled.fill(0)

    oled.text(line1, 0, 0)
    oled.text(line2, 0, 12)
    oled.text(line3, 0, 24)
    oled.text(line4, 0, 36)
    oled.text(line5, 0, 48)

    oled.show()

    select_mux_channel(255)


# -------------------------------------------------
# News Paging
# -------------------------------------------------

# Reading time per line
SECONDS_PER_LINE = 2

# Minimum and maximum time for one page
MIN_PAGE_TIME = 4
MAX_PAGE_TIME = 10


# Current news data
news_stories = []

# All pages created from the current stories
news_pages = []

# Current page number
news_page_index = 0

# Time the current page was displayed
news_last_update = 0

# How long the current page should stay visible
news_page_time = 0


# -------------------------------------------------
# Wrap Text
# -------------------------------------------------

def wrap_text(text, width=16):

    words = text.split()

    lines = []
    current_line = ""

    for word in words:

        # Handle words longer than the display width
        if len(word) > width:

            if current_line:
                lines.append(current_line)
                current_line = ""

            while len(word) > width:

                lines.append(word[:width])
                word = word[width:]

            current_line = word

        # Start a new line
        elif len(current_line) == 0:

            current_line = word

        # Word fits on current line
        elif len(current_line) + 1 + len(word) <= width:

            current_line += " " + word

        # Word does not fit
        else:

            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines


# -------------------------------------------------
# Build News Pages
# -------------------------------------------------

def build_news_pages(stories):

    pages = []

    for story in stories:

        lines = wrap_text(story)

        if not lines:
            lines = [""]

        # Four headline lines per page
        for start in range(0, len(lines), 4):

            page_lines = lines[start:start + 4]

            # Always make exactly four lines
            while len(page_lines) < 4:
                page_lines.append("")

            pages.append(page_lines)

    return pages


# -------------------------------------------------
# Calculate Dynamic Page Time
# -------------------------------------------------

def calculate_page_time(page):

    line_count = 0

    for line in page:

        if line.strip():
            line_count += 1

    # Two seconds per actual line
    page_time = line_count * SECONDS_PER_LINE

    # Minimum display time
    if page_time < MIN_PAGE_TIME:
        page_time = MIN_PAGE_TIME

    # Maximum display time
    if page_time > MAX_PAGE_TIME:
        page_time = MAX_PAGE_TIME

    return page_time


# -------------------------------------------------
# Draw News Page
# -------------------------------------------------

def display_news_page(page):

    oled = oleds[NEWS_DISPLAY]

    select_mux_channel(NEWS_DISPLAY)

    oled.fill(0)

    # Header
    oled.text("NEWS", 0, 0)

    # Four headline lines
    oled.text(page[0], 0, 10)
    oled.text(page[1], 0, 20)
    oled.text(page[2], 0, 30)
    oled.text(page[3], 0, 40)

    oled.show()

    select_mux_channel(255)


# -------------------------------------------------
# Start / Load New News
# -------------------------------------------------

def start_news(stories):

    global news_stories
    global news_pages
    global news_page_index
    global news_last_update
    global news_page_time

    # Save the new stories
    news_stories = stories

    # Turn all stories into pages
    news_pages = build_news_pages(stories)

    # Start at the first page
    news_page_index = 0

    if not news_pages:
        return

    # Calculate how long the first page should stay
    news_page_time = calculate_page_time(
        news_pages[news_page_index]
    )

    # Start the timer
    news_last_update = time.ticks_ms()

    # Display the first page
    display_news_page(
        news_pages[news_page_index]
    )


# -------------------------------------------------
# Update News Display
# -------------------------------------------------

def update_news():

    global news_page_index
    global news_last_update
    global news_page_time

    if not news_pages:
        return

    now = time.ticks_ms()

    elapsed = time.ticks_diff(
        now,
        news_last_update
    )

    # Has the current page been displayed long enough?
    if elapsed >= news_page_time * 1000:

        # Move to the next page
        news_page_index += 1

        # If we reached the end,
        # start again from the first page
        if news_page_index >= len(news_pages):

            news_page_index = 0

        # Calculate timing for the new page
        news_page_time = calculate_page_time(
            news_pages[news_page_index]
        )

        # Reset the timer
        news_last_update = now

        # Display the new page
        display_news_page(
            news_pages[news_page_index]
        )
