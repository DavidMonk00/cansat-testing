import board
import time
import busio
import adafruit_si7021
import adafruit_lis3mdl
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
import socket
from common.data_structures import Packet
import yaml
import datetime

SERVER_ADDRESS = "192.168.2.42"
SOCKET_PORT = 20001


def main():
    schema = yaml.safe_load(open("common/packet_structure.yml"))
    sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_si7021.SI7021(board.I2C())
    imu = LSM6DSOX(i2c)
    magnetometer = adafruit_lis3mdl.LIS3MDL(i2c)

    i = 0
    while True:
        p = Packet(
            schema, id=i,
            temperature=sensor.temperature, humidity=sensor.relative_humidity,
            acceleration=imu.acceleration, gyro=imu.gyro,
            B=magnetometer.magnetic, time=datetime.datetime.now()
        )
        sock.sendto(p.encode(), (SERVER_ADDRESS, SOCKET_PORT))
        time.sleep(1)
        i += 1


if __name__ == '__main__':
    main()
