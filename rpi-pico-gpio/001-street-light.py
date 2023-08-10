from machine import Pin
import time

red = Pin(19, Pin.OUT)
yellow = Pin(20, Pin.OUT)
green = Pin(21, Pin.OUT)

button = Pin(16, Pin.IN, Pin.PULL_DOWN)

red.on()
while True:
    if button.value() == 1:
        red.off()
        yellow.on()
        time.sleep_ms(500)
        yellow.off()
        green.on()
        time.sleep_ms(2500)
        green.off()
        yellow.on()
        time.sleep_ms(500)
        yellow.off()
        red.on()
