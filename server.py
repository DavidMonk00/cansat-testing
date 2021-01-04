import socket
import yaml
from common.data_structures import Packet

BIND_ADDRESS = "0.0.0.0"
PORT = 20001

sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
sock.bind((BIND_ADDRESS, PORT))
schema = yaml.safe_load(open("common/packet_structure.yml"))

while True:
    b = sock.recvfrom(1024)
    p = Packet.decode(schema, b[0])
    print("Packet: ({}) | From: {}".format(p, b[1]))
