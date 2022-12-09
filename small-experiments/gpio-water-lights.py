import RPi.GPIO as GPIO
import time

led_pins = [17, 18, 27, 22, 23, 24, 25, 2, 3, 8]


def init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_pins, GPIO.OUT)
    GPIO.output(led_pins, GPIO.HIGH)


def loop():
    while True:
        for pin in led_pins:
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(pin, GPIO.HIGH)

        for pin in led_pins[::-1]:
            GPIO.output(pin, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(pin, GPIO.HIGH)


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
