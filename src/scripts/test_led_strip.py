from gpiozero import PWMLED, LEDBoard
from math import cos, sin
from time import sleep
from enum import Enum
from typing import Optional

"""
    configure color based on GPIO pins
    GPIO 17 = 11 pin
    GPIO 22 = 15 pin
    GPIO 24 = 18 pin
"""
class LedColor(Enum):
    RED = 17
    GREEN = 22
    BLUE = 24

class PowerModeLed:
    def __init__(self, red: int, green: int, blue: int):
        self.red = PWMLED(red)
        self.green = PWMLED(green)
        self.blue = PWMLED(blue)

    def shades(self, x: int = 1, cycles: Optional[int] = None):
        if cycles is None:
            cycles = 400
        for i in range(cycles):
            # creating some cyclical randomness to change RGB combination
            self.green.value = abs(cos(i/10)*x)
            self.blue.value = abs(sin(i/10)*x)
            self.red.value = self.green.value * self.blue.value * x
            sleep(0.05)
            self.switch_off()

    def switch_off(self):
        self.red.off()
        self.green.off()
        self.blue.off()


class TestLedBoard:
    def __init__(self, red: int, green: int, blue: int):
        self.leds = LEDBoard(red, green, blue, pwm=True)

    def blink(self, cycles: Optional[int] = 10):
        self.leds.blink(on_time=0.2, off_time=0.2, n=cycles, background=False)
        self.leds.off()

    def pulse(self, cycles: Optional[int] = 10):
        self.leds.pulse(fade_in_time=0.2, fade_out_time=0.2, n=cycles, background=False)
        self.leds.off()

def test_led_board():
    leds = TestLedBoard(LedColor.RED.value, LedColor.BLUE.value, LedColor.GREEN.value)
    print("Blinking")
    leds.blink()
    sleep(1)
    print("Pulsing")
    leds.pulse()


if __name__ == '__main__':
    print("Testing PWMLED")
    led = PowerModeLed(LedColor.RED.value, LedColor.GREEN.value, LedColor.BLUE.value)
    led.shades(x=1, cycles=4)

    print("Testing LEDBoard")
    test_led_board()
