from machine import Pin, PWM, ADC
import time
import math

r_pwm = PWM(Pin(18), freq=2000, duty_u16=0)
g_pwm = PWM(Pin(19), freq=2000, duty_u16=0)
b_pwm = PWM(Pin(20), freq=2000, duty_u16=0)

r_adc = ADC(Pin(26))
g_adc = ADC(Pin(27))
b_adc = ADC(Pin(28))


def refresh_value(pwm, adc):
    value = adc.read_u16()
    if value > 64535:
        # make sure LED is fully off
        value = 65535
    else:
        value = 65535 - (65535 - value) // 3
    pwm.duty_u16(value)


while True:
    refresh_value(r_pwm, r_adc)
    refresh_value(g_pwm, g_adc)
    refresh_value(b_pwm, b_adc)
