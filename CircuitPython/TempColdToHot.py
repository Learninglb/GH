import time
from adafruit_circuitplayground import cp

TONE_PIANO = False

cp.pixels.auto_write = False
cp.pixels.brightness = 0.01

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (153, 0, 255)
PINK = (255, 102, 255)
WHITE = (255, 255, 255)
GREY = (153, 153, 153)

while True:
    vTemp = cp.temperature
    for i in range(10):
        if vTemp <= 20:
            cp.pixels.fill(GREY)
        else:
            if vTemp <= 22:
                cp.pixels.fill(BLUE)
            else:
                if vTemp <= 24:
                    cp.pixels.fill(GREEN)
                else:
                    if vTemp <= 26:
                        cp.pixels.fill(PINK)
                    else:
                        if vTemp <= 28:
                            cp.pixels.fill(YELLOW)
                        else:
                            if vTemp > 28:
                                cp.pixels.fill(RED)
        cp.pixels.show()
        time.sleep(0.05)
