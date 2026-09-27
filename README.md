# Dazzling2-mini
This is an automated data logger and display array. It uses two Raspberry Pi Pico 2 microcontrollers. Called Sender Pico and Receiver Pico, respectively. Sender's primary job is to gather data based on a predetermined schedule and determine what information to pass onto the Receiver Pico, before saving it for later analysis. Receiver Pico's primary job is to take the UART message from the Sender and then display it on one of its four 128 x 64 px OLED displays. 

The main 4 tasks that will be ran on it are:
- Weather updates
- Stock prices
- News headlines
- Date and Time

Future tasks:
- Calendar Reminders
- Screensavers

Potential Project Scope Additions:
- Integrated E-ink display for a weather map
- Encoder based menu navigation
- Small speaker
- FRAM
- More I2C devices such as the SSD1305 OLED, DAC, 8:1 analog switch, led lights


