#!/usr/bin/python3

# Copyright (C) 2020  Connor Czarnuch
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

'''
Load config file.
Load all sensors in config file.
Connect to server and get next time to update data.

At this time, read from sensors and upload data to server.
After time upload, sync from time server.
'''

import importlib
import time
import tools

CONFIG_FILE = 'config.cfg'

def main():
    # importList, sensorList = import_sensors()

    nextTime = int(get_new_time())
    print(time.time())
    print(nextTime)
    print()

    while True:
        while time.time() < nextTime:
            continue

        # data = read_from_all(sensorList)

        print("data") # like sending data to server for now

        nextTime = int(get_new_time())
        print(time.time())
        print(nextTime)
        print()

        # sync from time server


def import_sensors():
    """Imports sensor libraries and sensor objects from a config file.
    
    Returns:
        [list, list] -- Two lists of modules and sensor objects.
    """
    importList = []
    sensorList = []
    config = tools.load_config(CONFIG_FILE)

    for i, item in enumerate(config):
        if item[0] == "gps_coords":
            continue
        else:
            importList.append(importlib.import_module("sensors."+item[0]))
            sensorList.append(importList[i].create(address=item[1]))
    return importList, sensorList


def read_from_all(sensorList):
    """Iteratively read data from a list of sensor objects.
    
    Arguments:
        sensorList {Array of sensor Objects} -- A list containing an object for each of the sensors found in the config file.
    
    Returns:
        Array -- Multi-dimensional array containing the data read by the sensors.
    """
    sensor_data = []
    for data in sensorList:
        sensor_data.append(data.readAll())
    return sensor_data


def get_new_time():
    """Gets the latest time from the time server.
    
    Returns:
        Int -- Time for next data read in Unix time format.
    """
    nextTime = tools.get_data_from_server("http://localhost:8000/time.php")
    return nextTime[-1]


if __name__ == "__main__":
    main()