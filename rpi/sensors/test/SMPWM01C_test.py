import SMPWM01C
import pigpio

pi = pigpio.pi('localhost') # Connect to a remote pi or 'localhost'
# Select the pi GPIO pin that is connected to the sensor for PM25
# Select the pi GPIO pin that is connected to the sensor for PM10
# Make sure to use the Broadcom GPIO Pin number
        
sensor25 = SMPWM01C.sensor(pi, 17)
sensor10 = SMPWM01C.sensor(pi, 16)

if SMPWM01C.test(sensor25, sensor10):
    data = SMPWM01C.readAll(sensor25, sensor10)
    print(data)
    
pi.stop()