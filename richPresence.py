from f1_2020_telemetry.packets import *
from pypresence import Presence
import socket
import time

timer = int(round(time.time() * 1000))

udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_socket.settimeout(10.0)
udp_socket.bind(('', ))

client_id = ''
RPC = Presence(client_id)
RPC.connect()

def getPlayerIndex():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketLapData_V1):
            header = packet.header
            return header.playerCarIndex

def trackSwitch(argument):
    switcher = {
        0: "melbourne",
        1: "paulricard",
        2: "shanghai",
        3: "sakhir",
        4: "barcelona",
        5: "monaco",
        6: "montreal",
        7: "silverstone",
        8: "hockenheim",
        9: "hungaroring",
        10: "spa",
        11: "monza",
        12: "singapore",
        13: "suzuka",
        14: "yasmarina",
        15: "austin",
        16: "interlagos",
        17: "spielberg",
        18: "sochi",
        19: "mexico",
        20: "baku",
        21: "sakhir",
        22: "silverstone",
        23: "austin",
        24: "suzuka",
        25: "hanoi",
        26: "zandvoort"
    }
    return switcher.get(argument, "Invalid track.")

def getTrack():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketSessionData_V1):
            return trackSwitch(packet.trackId)

def teamSwitch(argument):
    switcher = {
        0: "mercedes",
        1: "ferrari",
        2: "redbullracing",
        3: "williams",
        4: "racingpoint",
        5: "renault",
        6: "alphatauri",
        7: "haas",
        8: "mclaren",
        9: "alfaromeo",
    }
    return switcher.get(argument, "Invalid team.")

def getCar():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketParticipantsData_V1):
            return teamSwitch(packet.participants[getPlayerIndex()].teamId)

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

def getPlayerPosition():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketLapData_V1):
            if(packet.lapData[getPlayerIndex()].carPosition==1):
                return str(packet.lapData[getPlayerIndex()].carPosition)+"st"
            if (packet.lapData[getPlayerIndex()].carPosition == 2):
                return str(packet.lapData[getPlayerIndex()].carPosition) + "nd"
            if (packet.lapData[getPlayerIndex()].carPosition == 3):
                return str(packet.lapData[getPlayerIndex()].carPosition) + "rd"
            else:
                return str(packet.lapData[getPlayerIndex()].carPosition) + "th"


def getNumberOfDrivers():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketParticipantsData_V1):
            return packet.numActiveCars


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
        if isinstance(packet, PacketLapData_V1):
            if(packet.lapData[getPlayerIndex()].bestLapTime==0.0):
                return "No lap time"
            else:
                return packet.lapData[getPlayerIndex()].bestLapTime


def showRacePresence():
    RPC.update(state=str(str(getPlayerPosition())+"/"+str(getNumberOfDrivers())),
               start=timer,
               details="Race | " +str(getLapNumber())+"/"+str(getTotalLapNumber())+" laps",
               large_image=str(getTrack()),
               small_image=str(getCar()),
               large_text="Track",
               small_text="Car")

def showQualiPresence(type):
    if(type=="ONE SHOT QUALI"):
        RPC.update(state=str(getPlayerPosition() + "/" + str(getNumberOfDrivers())),
                   start=timer,
                   details=type + " | " +getWeather(),
                   large_image=str(getTrack()),
                   small_image=str(getCar()),
                   large_text="Track",
                   small_text="Car")

    else:
        RPC.update(state=str(getPlayerPosition() + "/" + str(getNumberOfDrivers())),
                   start=timer,
                   details= type+" | Best lap: " +str(getBestLap()),
                   large_image=str(getTrack()),
                   small_image= str(getCar()),
                   large_text="Track",
                   small_text="Car")
def showTimeTrialPresence():
    RPC.update(state="Weather: "+getWeather(),
               start=timer,
               details= "Time Trial | "+str(getBestLap()),
               large_image = str(getTrack()),
               small_image= str(getCar()),
               large_text="Track",
               small_text="Car")

while True:
    try:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)

        if (isinstance(packet, PacketSessionData_V1)):
            if (packet.sessionType == 10):
                showRacePresence()
            elif (packet.sessionType == 5):
                showQualiPresence("Q1")
            elif (packet.sessionType == 6):
                showQualiPresence("Q2")
            elif (packet.sessionType == 7):
                showQualiPresence("Q3")
            elif (packet.sessionType == 8):
                showQualiPresence("SHORT QUALIFYING")
            elif (packet.sessionType == 9):
                showQualiPresence("ONE SHOT QUALI")
            elif (packet.sessionType == 12):
                showTimeTrialPresence()

    except socket.timeout:
        RPC.update(start=timer)



