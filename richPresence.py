from f1_2020_telemetry.packets import *
from pypresence import Presence
import socket
import time

client_id = ''
RPC = Presence(client_id, pipe=0)
RPC.connect()

timer = int(round(time.time() * 1000))

udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_socket.bind(('', ))

def getTrack():

def getCar():

def getWeather():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketSessionData_V1):
            if (packet.weather == 0):
                return "Sunny"
            elif (packet.weather == 1):
                return "Light Clouds"
            elif (packet.weather == 2):
                return "Overcast"
            elif (packet.weather == 3):
                return "Light Rain"
            elif (packet.weather == 4):
                return "Heavy Rain"
            elif (packet.weather == 5):
                return "Storm"

def getPlayerIndex():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketLapData_V1):
            header = packet.header
            return header.playerCarIndex
            break

def getPlayerPosition():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketLapData_V1):
            return packet.lapData[getPlayerIndex()].carPosition
            break

def getNumberOfDrivers():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketParticipantsData_V1):
            return packet.numActiveCars
            break

def getLapNumber():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketLapData_V1):
            return packet.lapData[getPlayerIndex()].currentLapNum

def getTotalLapNumber():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketSessionData_V1):
            return packet.totalLaps

def getBestLap():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketSessionData_V1):
            return packet.lapData[getPlayerIndex()].bestLapTime

def showRacePresence():
    RPC.update(state=str(str(getPlayerPosition())+" out of "+str(getNumberOfDrivers()))+" drivers",
               start=timer,
               details="Race | " +str(getLapNumber())+"/"+str(getTotalLapNumber())+" laps")
def showQualiPresence(type):
    if(type=="ONE SHOT QUALI"):
        RPC.update(state=str(str(getPlayerPosition()) + " out of " + str(getNumberOfDrivers())) + " drivers.",
                   start=timer,
                   details=type + " | " +getWeather())
    else:
        RPC.update(state=str(str(getPlayerPosition()) + " out of " + str(getNumberOfDrivers())) + " drivers.",
                   start=timer,
                   details= type+" | BEST LAP: " +getBestLap())
def showTimeTrialPresence():
    RPC.update(state="Weather:"+getWeather(),
               start=timer,
               details="BEST LAP: "+getBestLap())

while True:
    udp_packet = udp_socket.recv(2048)
    packet = unpack_udp_packet(udp_packet)

    if (isinstance(packet, PacketSessionData_V1)):
        # race
        if(packet.sessionType==10):
            showRacePresence()

        elif(packet.sessionType==5):
            showQualiPresence("Q1")
        elif(packet.sessionType==6):
            showQualiPresence("Q2")
        elif(packet.sessionType==7):
            showQualiPresence("Q3")
        elif(packet.sessionType==8):
            showQualiPresence("SHORT QUALIFYING")
        elif(packet.sessionType==9):
            showQualiPresence("ONE SHOT QUALIFYING")
        elif(packet.sessionType==12):
            showTimeTrialPresence()


