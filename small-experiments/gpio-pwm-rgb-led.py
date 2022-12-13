import RPi.GPIO as GPIO
import time
import random

pwm_pin_r = 17
pwm_pin_g = 27 
pwm_pin_b = 4
pwm_pins = [pwm_pin_r, pwm_pin_g, pwm_pin_b]
pwm_freq = 2000  # 2000 Hz


def init():
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
    (ro, go, bo) = (0, 0, 0)
    while True:
        (r, g, b) = (random.randint(0, 1) for _ in range(0, 3))
        
        if r == ro and g == go and b == bo:
            continue

        if not r and not g and not b:
            continue
       
        print(f"r={r}, g={g}, b={b}")

        for i in range(100, -1, -1):
            time.sleep(0.02)
            if r:
                pwm_r.ChangeDutyCycle(i)
            if g:
                pwm_g.ChangeDutyCycle(i)
            if b:
                pwm_b.ChangeDutyCycle(i)

        time.sleep(0.2)

        for i in range(0, 101, 1):
            time.sleep(0.02)
            if r:
                pwm_r.ChangeDutyCycle(i)
            if g:
                pwm_g.ChangeDutyCycle(i)
            if b:
                pwm_b.ChangeDutyCycle(i)

        (ro, go, bo) = (r, g, b)


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
    finally:
        destroy()
