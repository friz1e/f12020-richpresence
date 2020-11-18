from f1_2020_telemetry.packets import *
import socket
from pypresence import Presence

client_id = ''
RPC = Presence(client_id, pipe=0)
RPC.connect()

udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_socket.settimeout(1.0)
udp_socket.bind(('', ))

while True:
    try:
        udp_packet = udp_socket.recv(2048)
    except socket.timeout:
        continue

    packet = unpack_udp_packet(udp_packet)

    if (isinstance(packet, PacketSessionData_V1)):
        # race
        if(packet.sessionType==10):
        # q1
        elif(packet.sessionType==5):
        # q2
        elif(packet.sessionType==6):
        # q3
        elif(packet.sessionType==7):
        # short quali
        elif(packet.sessionType==8):
        # one shot quali
        elif(packet.sessionType==9):
        # time trial
        elif(packet.sessionType==12):

def getPlayerIndex():
    udp_packet = udp_socket.recv(2048)
    packet = unpack_udp_packet(udp_packet)
    if(isinstance(packet, PacketHeader)):
        return packet.playerCarIndex


