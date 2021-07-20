import I2C

SENSOR_ADDR = 0x00  # Change this to the i2c hex address specified by the sensor
I2C_CHANNEL = 1  # I2C channel to use


class SENSOR():
    def __init__(self, address=SENSOR_ADDR, i2c_ch=I2C_CHANNEL):
        self.address = address
        self._device = I2C.Device(address, i2c_ch)

        self.reset()  # Run the device reset command
        self.load_calibration()  # Load device calibration data

    def reset(self):
        """Reset device parameters
        :return True or False if device is reset successfully.
        """
        return True

    def load_calibration(self):
        """Load calibration data from constants if required.
        """
        return

    def test(self):
        """Run test to see if sensor is setup properly.
        :return True or False if test passes.
        """
        return True

    """
    In addition to these methods, please add methods to read and write to the sensor the appropriate data.
    """


def create(i2c_address=SENSOR_ADDR, i2c_channel=I2C_CHANNEL):
    sensor = SENSOR(i2c_address, i2c_channel)
    if not sensor.test():
        raise Exception
    return sensor
