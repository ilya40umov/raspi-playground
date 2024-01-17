from machine import Pin, Timer
import time


led_index = 0

leds = [Pin(21, Pin.OUT), Pin(20, Pin.OUT), Pin(19, Pin.OUT)]
button = Pin(16, Pin.IN, Pin.PULL_DOWN)
timer = Timer()


def on_button_press(pin: Pin):
    pin.irq(handler=None)
    global led_index
    if led_index + 1 < len(leds):
        led_index += 1
    else:
        led_index = 0
    timer.init(mode=Timer.ONE_SHOT, period=50, callback=add_handler)


def add_handler(timer: Timer):
    if button.value() == 0:
        button.irq(on_button_press, Pin.IRQ_RISING)
    else:
        timer.init(mode=Timer.ONE_SHOT, period=50, callback=add_handler)


add_handler(timer)
while True:
    time.sleep_ms(50)
    for i, led in enumerate(leds):
        if i == led_index:
            led.on()
        else:
            led.off()
