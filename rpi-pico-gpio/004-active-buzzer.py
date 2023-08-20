from machine import Pin
import time

# this pin is connected to a transistor
buzzer = Pin(19, Pin.OUT)

button = Pin(27, Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == 0:
        buzzer.on()
    else:
        buzzer.off()
    time.sleep_ms(10)
