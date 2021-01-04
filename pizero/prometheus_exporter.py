from prometheus_client import start_http_server, Gauge
import board
import time
import busio
import adafruit_si7021
import adafruit_lis3mdl
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX


def main():
    i2c = busio.I2C(board.SCL, board.SDA)

    g_temp = Gauge('i2c_temperature', 'Temperature of Si7021 module.')
    g_hum = Gauge('i2c_humidity', 'Relative humidity of Si7021 module.')
    g_mag_x = Gauge('i2c_mag_x', 'Magnetic Field Strength in X')
    g_mag_y = Gauge('i2c_mag_y', 'Magnetic Field Strength in Y')
    g_mag_z = Gauge('i2c_mag_z', 'Magnetic Field Strength in Z')
    g_accel_x = Gauge('i2c_accel_x', 'Acceleration in X')
    g_accel_y = Gauge('i2c_accel_y', 'Acceleration in Y')
    g_accel_z = Gauge('i2c_accel_z', 'Acceleration in Z')
    g_gyro_x = Gauge('i2c_gyro_x', 'Angular velocity in X')
    g_gyro_y = Gauge('i2c_gyro_y', 'Angular velocity in Y')
    g_gyro_z = Gauge('i2c_gyro_z', 'Angular velocity in Z')

    sensor = adafruit_si7021.SI7021(board.I2C())
    magnetometer = adafruit_lis3mdl.LIS3MDL(i2c)
    imu = LSM6DSOX(i2c)

    start_http_server(8000)
    while True:
        g_temp.set(sensor.temperature)
        g_hum.set(sensor.relative_humidity)
        mag_x, mag_y, mag_z = magnetometer.magnetic
        g_mag_x.set(mag_x)
        g_mag_y.set(mag_y)
        g_mag_z.set(mag_z)
        accel_x, accel_y, accel_z = imu.acceleration
        g_accel_x.set(accel_x)
        g_accel_y.set(accel_y)
        g_accel_z.set(accel_z)
        gyro_x, gyro_y, gyro_z = imu.gyro
        g_gyro_x.set(gyro_x)
        g_gyro_y.set(gyro_y)
        g_gyro_z.set(gyro_z)

        time.sleep(0.5)


if __name__ == '__main__':
    main()
