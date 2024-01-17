from machine import Pin, PWM
import time
import random

r = PWM(Pin(22), freq=2000, duty_u16=0)
g = PWM(Pin(21), freq=2000, duty_u16=0)
b = PWM(Pin(20), freq=2000, duty_u16=0)

steps = 30
max_value = 65535

while True:
    max_left = max_value
    r_v = random.randint(int(max_left * 0.01), int(max_left * 0.9))
    max_left -= r_v
    g_v = random.randint(int(max_left * 0.01), int(max_left * 0.9))
    max_left -= g_v
    b_v = max_left
    for i in range(2, steps + 1):
        r.duty_u16(max_value - int(i / steps * r_v))
        g.duty_u16(max_value - int(i / steps * g_v))
        b.duty_u16(max_value - int(i / steps * b_v))
        time.sleep_ms(50 + 50 * int(steps / (steps + i)))
    for i in range(steps, 2, -1):
        r.duty_u16(max_value - int(i / steps * r_v))
        g.duty_u16(max_value - int(i / steps * g_v))
        b.duty_u16(max_value - int(i / steps * b_v))
        time.sleep_ms(50 + 50 * int(steps / (steps + i)))
