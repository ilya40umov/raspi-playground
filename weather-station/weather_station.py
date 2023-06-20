#!/usr/bin/python
import time
import traceback
from sense_hat import SenseHat
from prometheus_client import start_http_server, Gauge

sense = SenseHat()

gauge_temperature = Gauge("home_weather_temperature", "Temperature in C")
gauge_humidity = Gauge("home_weather_humidity", "Humidity in %rH")
gauge_pressure = Gauge("home_weather_pressure", "Pressure in Millibars")

print("=== Started ===")

start_http_server(8000)

try:
    while True:
        temp_from_humidity = float(sense.get_temperature_from_humidity())
        temp_from_pressure = float(sense.get_temperature_from_pressure())
        temp_correction_factor = (
            temp_from_humidity - temp_from_pressure
        ) / temp_from_pressure
        humidity = float(sense.get_humidity())
        corrected_humidity = humidity * (1 - temp_correction_factor)
        gauge_temperature.set(round(temp_from_pressure, 2))
        gauge_humidity.set(round(corrected_humidity, 2))
        gauge_pressure.set(round(float(sense.get_pressure()), 2))
        time.sleep(5)
except Exception as e:
    print(e)
    traceback.print_exc()
finally:
    print("=== Finished ===")
