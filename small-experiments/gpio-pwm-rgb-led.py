import RPi.GPIO as GPIO
import time
import random

pwm_pin_r = 4
pwm_pin_g = 17
pwm_pin_b = 27
pwm_pins = [pwm_pin_r, pwm_pin_g, pwm_pin_b]
pwm_freq = 2000  # 2000 Hz


def init():
    global pwm_r, pwm_g, pwm_b

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwm_pins, GPIO.OUT)
    GPIO.output(pwm_pins, GPIO.HIGH)

    pwm_r = GPIO.PWM(pwm_pin_r, pwm_freq)
    pwm_r.start(0)
    pwm_g = GPIO.PWM(pwm_pin_g, pwm_freq)
    pwm_g.start(0)
    pwm_b = GPIO.PWM(pwm_pin_b, pwm_freq)
    pwm_b.start(0)


def loop():
    while True:
        r = random.randint(0, 100)
        g = random.randint(0, 100)
        b = random.randint(0, 100)
        pwm_r.ChangeDutyCycle(r)
        pwm_g.ChangeDutyCycle(g)
        pwm_b.ChangeDutyCycle(b)
        time.sleep(1)


def destroy():
    pwm_r.stop()
    pwm_g.stop()
    pwm_b.stop()
    GPIO.cleanup()


if __name__ == "__main__":
    print("Started...")
    init()
    try:
        loop()
    except KeyboardInterrupt:
        print("Stopped after a keyboard interrupt...")
        destroy()
