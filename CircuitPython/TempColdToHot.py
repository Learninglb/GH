import time
from adafruit_circuitplayground import cp

cp.pixels.auto_write = False
cp.pixels.brightness = 0.01

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
GREY = (153, 153, 153)

while True:
    vTemp = cp.temperature
    for i in range(10):
        if vTemp >= 20:
            cp.pixels.fill(PURPLE)
        # elif vTemp <= 22:
        #     cp.pixels.fill(BLUE)
        # elif vTemp <= 24:
        #     cp.pixels.fill(GREEN)
        # elif vTemp <= 26:
        #     cp.pixels.fill(YELLOW)
        # elif vTemp >= 27:
        #     cp.pixels.fill(RED)
        else:
            cp.pixels.fill(PURPLE)
        cp.pixels.show()
        time.sleep(0.05)
