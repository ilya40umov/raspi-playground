import RPi.GPIO as GPIO
import time


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(2, GPIO.OUT)
    GPIO.setup(3, GPIO.OUT)
    GPIO.setup(4, GPIO.OUT)
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(21, GPIO.IN)

    while True:
        if GPIO.input(21) == 0:
            for pin in range(2, 6):
                GPIO.output(pin, GPIO.HIGH)
                time.sleep(0.25)
                GPIO.output(pin, GPIO.LOW)
                time.sleep(0.25)
        time.sleep(0.001)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted.")
    finally:
        print("Running GPIO cleanup.")
        GPIO.cleanup()
