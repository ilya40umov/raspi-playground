import RPi.GPIO as GPIO
import time
from lib import adc

pwm_pin_r = 24
pwm_pin_g = 23
pwm_pin_b = 18
pwm_pins = [pwm_pin_r, pwm_pin_g, pwm_pin_b]
pwm_freq = 2000  # 2000 Hz

pwm_r = None
pwm_g = None
pwm_b = None

adc_module = None
value_r = None
value_g = None
value_b = None


def init():
    global adc_module

    adc_module = adc.detect_module()
    if not adc_module:
        exit(-1)

    global pwm_r, pwm_g, pwm_b

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwm_pins, GPIO.OUT)
    GPIO.output(pwm_pins, GPIO.HIGH)

    pwm_r = GPIO.PWM(pwm_pin_r, pwm_freq)
    pwm_r.start(100)
    pwm_g = GPIO.PWM(pwm_pin_g, pwm_freq)
    pwm_g.start(100)
    pwm_b = GPIO.PWM(pwm_pin_b, pwm_freq)
    pwm_b.start(100)


def loop():
    global value_r, value_g, value_b
    while True:
        value_0 = adc_module.read(0)
        value_1 = adc_module.read(1)
        value_2 = adc_module.read(2)
        if value_0 != value_r or value_1 != value_g or value_2 != value_b:
            value_r = value_0
            value_g = value_1
            value_b = value_2
            pwm_r.ChangeDutyCycle((255.0 - value_r) / 255.0 * 100.0)
            pwm_g.ChangeDutyCycle((255.0 - value_g) / 255.0 * 100.0)
            pwm_b.ChangeDutyCycle((255.0 - value_b) / 255.0 * 100.0)
            print("RGB: %d, %d, %d" % (value_r, value_g, value_b))
        time.sleep(0.1)


def destroy():
    if adc_module:
        adc_module.close()
    if pwm_r:
        pwm_r.stop()
    if pwm_g:
        pwm_g.stop()
    if pwm_b:
        pwm_b.stop()
    GPIO.cleanup()


if __name__ == "__main__":
    print("Started...")
    init()
    try:
        loop()
    except KeyboardInterrupt:
        print("Stopped after a keyboard interrupt...")
    finally:
        destroy()
