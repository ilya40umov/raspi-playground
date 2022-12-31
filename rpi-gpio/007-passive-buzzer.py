import RPi.GPIO as GPIO
import time
import math

buzzer_pin = 23
button_pin = 24

buzzer_on = False
buzzer_pwm = None


def init():
    global buzzer_pwm
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    buzzer_pwm = GPIO.PWM(buzzer_pin, 1)
    buzzer_pwm.start(0)


def loop():
    global buzzer_on
    while True:
        if GPIO.input(button_pin) == GPIO.LOW:
            start_beep()
            if not buzzer_on:
                buzzer_on = True
                print("Buzzer on")
        else:
            stop_beep()
            if buzzer_on:
                buzzer_on = False
                print("Buzzer off")
        time.sleep(0.01)


def start_beep():
    buzzer_pwm.start(50)
    for x in range(0, 361):
        sin_value = math.sin(x * (math.pi / 180.0))
        tone_value = 2000 + sin_value * 500
        buzzer_pwm.ChangeFrequency(tone_value)
        time.sleep(0.001)


def stop_beep():
    buzzer_pwm.stop()


def destroy():
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
