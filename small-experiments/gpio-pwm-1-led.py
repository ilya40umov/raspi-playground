import RPi.GPIO as GPIO
import time

pwm_pin = 18
pwm_freq = 500  # 500 Hz


def init():
    global pwm

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pwm_pin, GPIO.OUT)
    GPIO.output(pwm_pin, GPIO.LOW)

    pwm = GPIO.PWM(pwm_pin, pwm_freq)
    pwm.start(0)  # initial duty cycle - 0%


def loop():
    while True:
        for duty_cycle in range(0, 101, 1):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.02)
        time.sleep(1)

        for duty_cycle in range(100, -1, -1):
            pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.02)
        time.sleep(1)


def destroy():
    pwm.stop()
    GPIO.cleanup()


if __name__ == "__main__":
    print("Started...")
    init()
    try:
        loop()
    except KeyboardInterrupt:
        print("Stopped after a keyboard interrupt...")
        destroy()
