#!/usr/bin/python3

# Copyright (C) 2020  Connor Czarnuch, with use of pimoroni BME680 library by Philip Howard.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import bme680

BME680_ADDR = 0x77
I2C_CHANNEL = 1


class BME680(bme680.BME680):
    def __init__(self, address=BME680_ADDR, i2c_ch=I2C_CHANNEL):
        super().__init__(address)
    
        # Load calibration values
        self._load_calibration()

        # Perform initial read
        self.readAll()

    def _load_calibration(self):
        self.set_humidity_oversample(bme680.OS_2X)
        self.set_pressure_oversample(bme680.OS_4X)
        self.set_temperature_oversample(bme680.OS_8X)
        self.set_filter(bme680.FILTER_SIZE_3)
        self.set_gas_status(bme680.ENABLE_GAS_MEAS)

        self.set_gas_heater_temperature(320)
        self.set_gas_heater_duration(150)
        self.select_gas_heater_profile(0)

    def readAll(self, temperature=True, humidity=True, pressure=True, gas=True):
        if self.get_sensor_data():
            data = {}
            if temperature:
                data['temperature'] = self.data.temperature
            if humidity:
                data['humidity'] = self.data.humidity
            if pressure:
                data['pressure'] = self.data.pressure
            if gas and self.data.heat_stable:
                data['gas'] = self.data.gas_resistance
            return data
    
    def test(self):
        status = self.get_sensor_data()
        if status:
            return True
        else:
            return False

def create(i2c_address=BME680_ADDR, i2c_channel=I2C_CHANNEL):
    sensor = BME680(i2c_address)
    if not sensor.test():
        raise Exception
    return sensor