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

import os
import time
import tools


CONFIG_FILE = os.getcwd() + '/config.cfg'
ADD_DATA_URL = 'http://localhost/add_data.php'


def main():
    sensorList = tools.import_sensors()

    nextTime = int(get_new_time())

    while True:
        while time.time() < nextTime:
            continue
        
        # Read and format sensor data
        data = read_from_all(sensorList)
        dataToSend = tools.format_dict(data)

        # Send data to server
        print(dataToSend)
        tools.send_data_to_server(ADD_DATA_URL, dataToSend)

        # Calculate next time to retrieve information
        nextTime = int(get_new_time())

        # sync from time server


def read_from_all(sensorList):
    """Iteratively read data from a list of sensor objects.
    
    Arguments:
        sensorList {Array of sensor Objects} -- A list containing an object for each of the sensors found in the config file.
    
    Returns:
        Array -- Multi-dimensional array containing the data read by the sensors.
    """
    sensor_data = []
    for sensor in sensorList:
        sensor_data.append(sensor.readAll())
    return sensor_data


def get_new_time(interval=300):
    """Calculate the next time based on the time interval given.
    
    Keyword Arguments:
        interval {int} -- The number of seconds between each interval. (default: {300})
    
    Returns:
        int -- Next time based on interval in Unix format.
    """
    curr_time = time.time()
    next_time = curr_time - (curr_time % interval) + interval
    return next_time


if __name__ == "__main__":
    main()