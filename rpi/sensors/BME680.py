#!/usr/bin/python3
#to install library, run 'sudo pip3 install adafruit-circuitpython-bme680'

from busio import I2C
import I2C_BME
import time
import board

# Create library object using our Bus I2C port
#i2c = I2C(board.SCL, board.SDA)
#bme680 = I2C_BME.Adafruit_BME680_I2C(i2c)
bme680 = I2C_BME.create()

# change this to match the location's pressure (hPa) at sea level
bme680.sea_level_pressure = 1032.0 #set for Hamilton, urban areas.

#returns in Celsius
def getTemperature():
    return bme680.temperature

#Returns in ohms
def getGas():
    return bme680.gas

#Returns as a percentage
def getHumidity():
    return bme680.humidity

#Returns in hPa
def getPressure():
    return bme680.pressure

#Returns in meters above sea level
def getAltitude():
    return bme680.altitude

def runForever():
    while True:
        print("\nTemperature: %0.1f C" % bme680.temperature)
        print("Gas: %d ohm" % bme680.gas)
        print("Humidity: %0.1f %%" % bme680.humidity)
        print("Pressure: %0.3f hPa" % bme680.pressure)
        print("Altitude = %0.2f meters" % bme680.altitude)

        time.sleep(2)



