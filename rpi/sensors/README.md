# To add a new sensor to the list

1. Make sure that the sensor supports I2C communication.
2. Create a new file with the name of the sensor and the .py extension marking it as a python file.
3. Start with the SENSOR.py file for the interface to the main program and add all methods necessarry to work with the new sensor.
4. Add the sensor support in the ../tools.py file.
5. Add any additional columns to the SQL database init script. Or, if deployed, add to the database itself.
