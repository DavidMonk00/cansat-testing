import board
import busio
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from datetime import datetime
from copy import deepcopy


def testRate(imu, rate):
    imu.accelerometer_data_rate = rate
    start = datetime.now()
    accel = deepcopy(imu.acceleration)
    while imu.acceleration == accel:
        pass
    end = datetime.now()
    return 1/float((end - start).total_seconds())


i2c = busio.I2C(board.SCL, board.SDA)
imu = LSM6DSOX(i2c)
for i in range(1, 12):
    print(i, testRate(imu, i))

