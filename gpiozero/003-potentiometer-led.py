from gpiozero import MCP3008, PWMLED
from time import sleep


def main():
    pot = MCP3008(channel=0)
    led = PWMLED(21)

    pot_value = None

    while True:
        new_pot_value = pot.value
        if pot_value != new_pot_value:
            pot_value = new_pot_value
        led.value = 1 - pot_value
        sleep(0.1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Program interrupted.")
