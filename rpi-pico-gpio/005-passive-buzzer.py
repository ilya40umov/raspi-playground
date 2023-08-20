from machine import Pin, PWM
import time
import math

# this pin is connected to a transistor
buzzer = PWM(Pin(19), freq=2000, duty_u16=0)

button = Pin(27, Pin.IN, Pin.PULL_UP)

while True:
    if button.value() == 0:
        buzzer.duty_u16(65535 // 2)
        for x in range(0, 361):
            sin_value = int(math.sin(x * (math.pi / 180.0)))
            tone_value = 2000 + sin_value * 1000
            buzzer.freq(tone_value)
            time.sleep_ms(10)
    else:
        buzzer.duty_u16(0)

    time.sleep_ms(10)
