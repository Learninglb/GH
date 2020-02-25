import time
from adafruit_circuitplayground.express import cpx
# Objects to Circuit Playground Express objects can now be
# referred to their abbreviated form
button_read = cpx.button_a
while True:
    cpx.red_led = True
    time.sleep(1)
    cpx.red_led = False
    time.sleep(1)
