#!/usr/bin/python
import time
from sense_hat import SenseHat

sense = SenseHat()
pixels = [[0, 0, 0] for i in range(8 * 8)]
sense.set_pixels(pixels)
