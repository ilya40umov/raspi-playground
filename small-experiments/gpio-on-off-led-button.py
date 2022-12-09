import RPi.GPIO as GPIO
import time


light_on = False


def on_button_press(channel):
    global light_on
    light_on = not light_on
    if light_on:
        GPIO.output(6, GPIO.HIGH)
    else:
        GPIO.output(6, GPIO.LOW)


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(12, GPIO.IN)

    GPIO.add_event_detect(12, GPIO.FALLING, on_button_press, 300)

    while True:
        time.sleep(0.001)


if __name__ == "__main__":
    try:
        main()
    finally:
        GPIO.cleanup()
