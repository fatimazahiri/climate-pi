#!/usr/bin/python3

# Author: Connor Czarnuch
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import re


def load_config(path="config.cfg"):
    """Load the GPS coordinates and I2C sensor data for the raspberry pi, returning the result as a dictionary.

    Keyword Arguments:
        path {str} -- The path to the config file. (default: {"config.cfg"})

    Returns:
        dict -- Dictionary containing the raspberry pi configuration.
    """
    try:
        cfg_file = open(path, 'r', encoding="utf-8")
        gps_coords = cfg_file.readline().strip()
        # Match the first read line with a regular expression for valid GPS coordinates
        prog = re.match("^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),\s*[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$",
                        gps_coords)
        if not prog:
            raise ValueError

    except IOError as e:
        print("Incorrect file path, does the config file exist?\n")
        print(e)
    except ValueError as e:
        print("Incorrect format for GPS coordinates! Are they there? Are they valid?")
    finally:
        cfg_file.close()
        return

    # If valid, split coordinates into array and store in the dict
    config = {"gps_coords": gps_coords.split(',')}

    # For each sensor, read line and add to dict
    sensor_data = cfg_file.readline()
    while sensor_data != '':
        line = sensor_data.strip().split(',')
        if len(line) > 1:
            config[line[0]] = line[1]
        elif len(line) == 1:
            config[line[0]] = None
        sensor_data = cfg_file.readline()

    cfg_file.close()
    return config


def format_array():
    pass


def send_data_to_server(url):
    pass


def get_data_from_server():
    pass


def force_sync_time():
    pass
