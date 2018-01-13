# Import necessary libraries
import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711

# Initialize load cell
hx = HX711(5, 6)
hx.set_reading_format("LSB", "MSB")
hx.set_reference_unit(92)       # Calibrate reference unit to 1g
hx.reset()
hx.tare()

def measure_sink():
    try:
        val = hx.get_weight(5)
        print(val)

        hx.power_down()
        hx.power_up()
        time.sleep(.01)
    except (KeyboardInterrupt, SystemExit):
        GPIO.cleanup()
        print("Exiting..")
        sys.exit()


while True:
    measure_sink()
