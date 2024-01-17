from gpiozero import LED, Button
from signal import pause


light_on = False


def on_button_press():
    global light_on
    light_on = not light_on
    if light_on:
        led.on()
        print("LED - on")
    else:
        led.off()
        print("LED - off")


def main():
    global led
    led = LED(17)

    button = Button(26)
    button.when_pressed = on_button_press

    print("Waiting for a button on pin 26 to be pulled down...")
    pause()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted.")
