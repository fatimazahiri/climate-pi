#!/usr/bin/env python

####### Instructions ########################
# On the Raspbery Pi make sure to install pigpio using Apt
# $ sudo apt-get install pigpio python-pigpio python3-pigpio
#
# Once installed make sure to run the pidpio daemon before
# running this script
#
# $ sudo pigpiod
# $ python pidustsensor.py
# or
# $ python3 pidustsensor.py
#
# Other packages to install for storing the data and presenting graph data
# $ sudo apt-get install python python3 python3-matplotlib python-matplotlib python3-flask python-flask python3-numpy python-numpy nano git lighttpd sqlite3 sqlite3-dev

####### Wiring Options ######################
# +-----------------------------------------+
#  |                                         |
#  |  Shinyei PPD42NS  / Grove Dust Sensor   |
#  |  (Sensor components facing you          |           
#  |                                         |
#  |    |+|        |+|                       |          
#  |    SL2 POT    CN1 POT                   |
#  +-----------------------------------------+
#  |    Pin Number                           |
#  |                                         |          
#  |     |     |     |     |     |           |
#  |     5     4     3     2     1           |       
#  |     |     |     |     |     |           |
#  +-----------------------------------------+
#        |     |     |     |     | 
#        |     |     |     |  GND (Black)
#        |     |     |     |     | 
#        |     |  5V (Red) |     | 
#        |     |     |     |     | 
#        |   PM2.5   |     |     |
#        |     |     |     |     | 
#        |     |     |   PM1.0   |
#        |     |     |     |     |
#   Threshold  |     |     |     |
#   for Pin 2  |     |     |     | 
#        |     |     |     |     | 
#        |     |     |     |     | 
#
# CN : S5B-EH(JST)
# 1 : COMMON(GND) [Black Wire on Grove Sensor]
# 2 : OUTPUT(P2) [Not used on Grove Connectr] [Can be used for PM1.0]
# 3 : INPUT(5VDC 90mA) [Red Wire on Grove Sensor]
# 4 : OUTPUT(P1) [Yellow Wire on Grove Sensor] [Used for PM2.5 mesurements]
# 5 : INPUT(T1)FOR THRESHOLD FOR [P2] [Not used on Grove Connector]
#############################################

from __future__ import print_function
import math
import pigpio
from datetime import datetime
import time

class sensor:

    def __init__(self, pi, gpio):
        
        self.pi = pi
        self.gpio = gpio
        
        self._start_tick = None
        self._last_tick = None
        self._low_ticks = 0
        self._high_ticks = 0

        pi.set_mode(gpio, pigpio.INPUT)

        self._cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cbf)

    # Method for calculating Ratio and Concentration
    def read(self):
        """
        Calculates the percentage low pulse time and calibrated
        concentration in particles per 1/100th of a cubic foot
        since the last read.

        For proper calibration readings should be made over
        30 second intervals.
        
        Returns a tuple of gpio, percentage, and concentration.
        """
        interval = self._low_ticks + self._high_ticks

        if interval > 0:
            ratio = float(self._low_ticks)/float(interval)*100.0
            conc = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62;
        else:
            ratio = 0
            conc = 0.0

        self._start_tick = None
        self._last_tick = None
        self._low_ticks = 0
        self._high_ticks = 0

        return (self.gpio, ratio, conc)

    def _cbf(self, gpio, level, tick):

        if self._start_tick is not None:

            ticks = pigpio.tickDiff(self._last_tick, tick)

            self._last_tick = tick

            if level == 0: # Falling edge.
                self._high_ticks = self._high_ticks + ticks

            elif level == 1: # Rising edge.
                self._low_ticks = self._low_ticks + ticks

            else: # timeout level, not used
                pass

        else:
            self._start_tick = tick
            self._last_tick = tick
         


def readAll(s25, s10):

    # pi = pigpio.pi('localhost') # Connect to a remote pi or 'localhost'

    # Select the pi GPIO pin that is connected to the sensor
    # For PM2.5 Readings, connected to Pin 4 of the Sensor
    # Make sure to use the Broadcom GPIO Pin number
    #s25 = sensor(pi, 17)

    # Select the pi GPIO pin that is connected to the sensor
    # For PM10 Readings, connected to Pin 2 of the Sensor
    # Make sure to use the Broadcom GPIO Pin number
    #s10 = sensor(pi, 16)
        
    time.sleep(30) # Use 30 for a properly calibrated reading.

    # Get the current time of the reading
    timestamp = datetime.now()
    
    # Read the PM2.5 values from the sensor
    # get the gpio, ratio and concentration in particles / 0.01 ft3
    g25, r25, c25 = s25.read()

    # do some checks on the concentration reading and print errors
    if (c25 == 1114000.62):
        print("PM2.5 Concentration Error\n")
        quit
  
    if c25 < 0:
        raise ValueError('Concentration cannot be a negative number')
        quit


    # Read the PM10 values from the sensor
    # get the gpio, ratio and concentration in particles / 0.01 ft3
    g10, r10, c10 = s10.read()
    
    # do some checks on the concentration reading and print errors
    if (c10 == 1114000.62):
        print("PM10 Concentration Error\n")
        quit
  
    if c10 < 0:
        raise ValueError('Concentration cannot be a negative number')
        quit


    # Special Calculations for differentiating between two particulate sizes
    # Note: Not sure why P10 calculation is subtracted from PM2.5
    # Maybe hreshold input (IN1) is left unsed, but it will be used later as a way to
    # split particule by size, and hence detect both PM10 and PM2.5 particules.
    PM10count = c10         # Not sure if this should be c10 only
    PM25count = c25         # Not sure if c25 - c10 is required instead


    # Convert conentrations to ug/ metre cubed
    # Convert concentration of PM2.5 and PM10 particles per 0.01 cubic feet to ug/ metre cubed
    # this method outlined by Drexel University students (2009) and is an approximation
    # does not contain correction factors for humidity and rain

    # Assume all particles are spherical, with a density of 1.65E12 ug/m3
    density = 1.65 * math.pow(10, 12)

    # PM2.5 Values
    # Assume the radius of a particle in the PM2.5 channel is .44 um
    rpm25 = 0.44 * math.pow(10, -6)

    # Volume of a PM2.5 sphere = 4/3 * pi * radius^3
    volpm25 = (4/3) * math.pi * (rpm25**3)

    # mass = density * volume
    masspm25 = density * volpm25

    # parts/m3 =  parts/foot3 * 3531.5
    # ug/m3 = parts/m3 * mass in ug
    concentration_ugm3_pm25 = PM25count * 3531.5 * masspm25 # or use c25 instead of PM25count


    # PM10 Values
    # Assume the radius of a particle in the PM10 channel is 2.6 um
    rpm10 = 2.6 * math.pow(10, -6)

    # Volume of a PM10 sphere = 4/3 * pi * radius^3
    volpm10 = (4/3) * math.pi * (rpm10**3)

    # mass = density * volume
    masspm10 = density * volpm10

    # parts/m3 =  parts/foot3 * 3531.5
    # ug/m3 = parts/m3 * mass in ug
    concentration_ugm3_pm10 = PM10count * 3531.5 * masspm10 # Or use c10 instead of PM10count




    # Convert concentration of PM2.5 particles in ug/ metre cubed to the USA 
    # Environment Agency Air Quality Index - AQI
    # https://en.wikipedia.org/wiki/Air_quality_index
    # Computing_the_AQI
    # https://github.com/intel-iot-devkit/upm/pull/409/commits/ad31559281bb5522511b26309a1ee73cd1fe208a?diff=split
    # input should be 24 hour average of ugm3, not instantaneous reading


    cbreakpointspm25 = [ [0.0, 12, 0, 50],\
                    [12.1, 35.4, 51, 100],\
                    [35.5, 55.4, 101, 150],\
                    [55.5, 150.4, 151, 200],\
                    [150.5, 250.4, 201, 300],\
                    [250.5, 350.4, 301, 400],\
                    [350.5, 500.4, 401, 500], ]
                
    C = concentration_ugm3_pm25

    if C > 500.4:
        aqi25 = 500

    else:
        for breakpoint in cbreakpointspm25:
            if breakpoint[0] <= C <= breakpoint[1]:
                Clow25 = breakpoint[0]
                Chigh25 = breakpoint[1]
                Ilow25 = breakpoint[2]
                Ihigh25 = breakpoint[3]
                aqi25 = (((Ihigh25-Ilow25)/(Chigh25-Clow25))*(C-Clow25))+Ilow25



    # Convert concentration of PM10 particles in ug/ metre cubed to the USA 
    # Environment Agency Air Quality Index - AQI
    # https://en.wikipedia.org/wiki/Air_quality_index
    # Computing_the_AQI
    # https://github.com/intel-iot-devkit/upm/pull/409/commits/ad31559281bb5522511b26309a1ee73cd1fe208a?diff=split
    # input should be 24 hour average of ugm3, not instantaneous reading


    cbreakpointspm10 = [ [0, 54, 0, 50],\
                    [55, 154, 51, 100],\
                    [155, 254, 101, 150],\
                    [255, 354, 151, 200],\
                    [355, 424, 201, 300],\
                    [425, 504, 301, 400],\
                    [505, 604, 401, 500], ]
                
    D = concentration_ugm3_pm10

    if D > 604:
        aqi10 = 500

    else:
        for breakpoint in cbreakpointspm10:
            if breakpoint[0] <= D <= breakpoint[1]:
                Clow10 = breakpoint[0]
                Chigh10 = breakpoint[1]
                Ilow10 = breakpoint[2]
                Ihigh10 = breakpoint[3]
                aqi10 = (((Ihigh10-Ilow10)/(Chigh10-Clow10))*(D-Clow10))+Ilow10

    data = {}
    if timestamp:
        data['timestamp'] = timestamp
    if r25:
        data['ratio25'] = r25
    if int(c25):
        data['conc25'] = str(int(c25))
    if int(PM25count):
        data['pm25count'] = str(int(PM25count))
    if int(concentration_ugm3_pm25):
        data['pm25metric'] = str(int(concentration_ugm3_pm25))
    if int(aqi25):
        data['aqi25'] = str(int(aqi25))
    if r10:
        data['ratio10'] = r10
    if int(c10):
        data['conc10'] = str(int(c10))
    if int(PM10count):
        data['pm10count'] = str(int(PM10count))
    if int(concentration_ugm3_pm10):
        data['pm10metric'] = str(int(concentration_ugm3_pm10))
    if int(aqi10):
        data['aqi10'] = str(int(aqi10))
 
    # Print
    #print(data)
    #pi.stop() # Disconnect from Pi.
    #print('test!!!!!!!!!!!!!')
    
    return data

def test(s25, s10):
    if s25 and s10:
        return True
    else:
        return False
    
