#!/usr/bin/python
import time
import traceback
from sense_hat import SenseHat
from prometheus_client import start_http_server, Gauge

sense = SenseHat()

gauge_temperature = Gauge('home_weather_temperature', 'Temperature in C')
gauge_humidity = Gauge('home_weather_humidity', 'Humidity in %rH')
gauge_pressure = Gauge('home_weather_pressure', 'Pressure in Millibars')

print("=== Started ===")

start_http_server(8000)

try:
    while True:
        gauge_temperature.set(round(float(sense.get_temperature()), 2))
        gauge_humidity.set(round(float(sense.get_humidity()), 2))
        gauge_pressure.set(round(float(sense.get_pressure()), 2))
        time.sleep(5)
except Exception as e:
    print(e)
    traceback.print_exc()
finally:
    print("=== Finished ===")
