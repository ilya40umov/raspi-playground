import RPi.GPIO as GPIO
import time

buzzer_pin = 23
button_pin = 24

buzzer_on = False


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buzzer_pin, GPIO.OUT)
    GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def loop():
    global buzzer_on
    while True:
        if GPIO.input(button_pin) == GPIO.LOW:
            GPIO.output(buzzer_pin, GPIO.HIGH)
            if not buzzer_on:
                buzzer_on = True
                print("Buzzer on")
        else:
            GPIO.output(buzzer_pin, GPIO.LOW)
            if buzzer_on:
                buzzer_on = False
                print("Buzzer off")
        time.sleep(0.01)


def destroy():
    GPIO.cleanup()


if __name__ == "__main__":
    print("Started...")
    init()
    try:
        loop()
    except KeyboardInterrupt:
        print("Stopped after a keyboard interrupt...")
        destroy()
