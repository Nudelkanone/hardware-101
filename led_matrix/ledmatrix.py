"""
This module shows how to use an 5x7 led matrix. It contains a class LedMatrix
that can be used to easily access a matrix.

Pinout of the matrix:

1 +---+ 12
2 |   | 11
3 |   | 10
4 |   | 9
5 |   | 8
6 +---+ 7

Connections: Electrical current travels from rows to columns.

     1
   13078
12 ooooo ^
11 ooooo |
 2 ooooo |
 9 ooooo |
 4 ooooo |
 5 ooooo |
 7 ooooo |
   ---->
"""

import RPi.GPIO as GPIO
import time


class LedMatrix:

    def __init__(self, boardmode=GPIO.BCM):
        """Create an led matrix. Use the connect-method afterwards to connect
        led matrix pins with GPIO pins on the Raspberry Pi."""

        # a dictionary that holds led pins of the matrix and corresponding
        # GPIO pin on the Raspberry Pi.
        self.led_gpio = {}

        # default pins on a 5x7 matrix
        self.x_pins = [1, 3, 10, 7, 8]
        self.y_pins = [12, 11, 2, 9, 4, 5, 6]

        # using the given numbering scheme
        GPIO.setmode(boardmode)        

    def connect_pins(self, ledpin, gpiopin):
        """Connect a Pin of the LED Matrix to a GPIO pin on the Raspberry
        Pi."""
        self.led_gpio[ledpin] = gpiopin

        # configure all pins as output
        GPIO.setup(gpiopin, GPIO.OUT)

    def led_pins_set(self, led_pins, on_off):
        """Turn the specified pin numbers on the LED Matrix on or off."""
        gpiopins = []
        for pinnr in led_pins:
            gpiopins.append(self.led_gpio[pinnr])

        GPIO.output(gpiopins, on_off)

    def on(self, x, y):
        """Turn the led at coordinate (x,y) on. Starting with (0,0) at
        top left. Multiple LEDs that are not all in one row/column cannot be
        handled this way. Use multiplexing instead - as described here
        https://www.mikrocontroller.net/articles/LED-Matrix#Multiplexbetrieb"""

        # first turn all off
        self.led_pins_set(self.led_gpio.keys(), False)

        # electric current can only travel from column (y) to row (x)
        ledp_hi_y = self.y_pins[y]
        ledp_lo_x = self.x_pins[x]

        # collect pins that must be high
        # determine GPIO pins for led pins
        led_pins_h = [ledp_hi_y]
        for ledpin in self.led_gpio:
            if ledpin in self.x_pins and ledpin != ledp_lo_x:
                led_pins_h.append(ledpin)

        self.led_pins_set(led_pins_h, True)


def main():
    """
     Connect four pins of the led-matrix to GPIO-pins and run a demo programm.

      -------+            +----------
             |            |
             +-1  ---  17-+
       LED   +-3  ---  18-+ Raspberry
      Matrix +-11 ---  23-+ Pi
             +-12 ---  22-+ 
             |            |
      -------+            +-----------
    """
    ledmat = LedMatrix()
    ledmat.connect_pins(ledpin=1, gpiopin=17)
    ledmat.connect_pins(ledpin=3, gpiopin=18)
    ledmat.connect_pins(ledpin=11, gpiopin=23)
    ledmat.connect_pins(ledpin=12, gpiopin=22)

    # turn on each of the 4 LEDs from top left to bottom right - for 5 seconds
    start = time.time()
    while time.time() - start < 5:
        for y in (0, 1):
            for x in (0, 1):
                ledmat.on(x, y)
                time.sleep(0.2)

    # turning on two leds at (0,0) and (0,1) at the same time 
    # using multiplexing
    fps = 120  # Hz
    sleeptime_per_pixel = 1/fps/4  # divide by 4 since using four pixels
    while True:
        for x in (0, 1):
            for y in (0, 1):
                if (x, y) in [(0, 0), (1, 1)]:
                    ledmat.on(x, y)

                time.sleep(sleeptime_per_pixel)


if __name__ == "__main__":
    main()
