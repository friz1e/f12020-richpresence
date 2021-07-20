from f1_2020_telemetry.packets import *
from pypresence import Presence
import socket
import time
import os
import psutil

while not "Discord.exe" in (p.name() for p in psutil.process_iter()):
        continue
while not "F1_2020_dx12.exe" in (p.name() for p in psutil.process_iter()):
        continue

udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
udp_socket.settimeout(10.0)
udp_socket.bind(('localhost', 20777))

client_id = ''
RPC = Presence(client_id)
RPC.connect()
RPC.update(large_image="f12020", details="Idling")

def seconds2time(sec, n_msec=3):
    if hasattr(sec,'__len__'):
        return [seconds2time(s) for s in sec]
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    pattern = '%%02d:%%0%d.%df' % (n_msec+3, n_msec)
    return ('' + pattern) % (m, s)

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
        41: "multiplayercar",
        255: "myteamcar"
    }
    return switcher.get(argument, "Invalid car.")

def teamInCorrectFormat(argument):
    switcher = {
        "mercedes": "Mercedes",
        "ferrari": "Ferrari",
        "redbullracing": "Red Bull Racing",
        "williams": "Williams",
        "racingpoint": "Racing Point",
        "renault": "Renault",
        "alphatauri": "Alpha Tauri",
        "haas": "Haas",
        "mclaren": "McLaren",
        "alfaromeo": "Alfa Romeo",
        "classicf1car": "Classic F1 Car",
        "f2car": "F2 Car",
        "multiplayercar": "Multiplayer Car",
        "myteamcar": "My Team Car"
    }
    return switcher.get(argument, "Invalid team.")

def getCarType():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketCarStatusData_V1):
            if packet.carStatusData[getPlayerIndex()].actualTyreCompound == 9 or packet.carStatusData[getPlayerIndex()].actualTyreCompound == 10:
                return "classicf1car"
            elif 11 <= packet.carStatusData[getPlayerIndex()].actualTyreCompound <= 15:
                return "f2car"
            else :
                return "f1car"

def getCar():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketParticipantsData_V1):
            if (getCarType() == "f1car"):
                return teamSwitch(packet.participants[getPlayerIndex()].teamId)
            elif (getCarType() == "classicf1car"):
                return "classicf1car"
            elif (getCarType() == "f2car"):
                return "f2car"

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
                return seconds2time(packet.lapData[getPlayerIndex()].bestLapTime, 3)

def isUserSpectating():
    while True:
        udp_packet = udp_socket.recv(2048)
        packet = unpack_udp_packet(udp_packet)
        if isinstance(packet, PacketSessionData_V1):
            if (packet.isSpectating == 1):
                return True
            else:
                return False

def showRacePresence():
    if(isUserSpectating()==True):
            RPC.update(state=str(getTotalLapNumber())+" laps | "+getWeather(),
                       details=str(("Spectating "+str(getNumberOfDrivers()) + " driver") if getNumberOfDrivers()==1 else ("Spectating "+str(getNumberOfDrivers()) + " drivers")),
                       large_image=str(getTrack()),
                       large_text="Track")

    elif (getTotalLapNumber() < getLapNumber()):
        RPC.update(state=str(str(getPlayerPosition()) + "/" + str(getNumberOfDrivers())+" | "+getWeather()),
                   details="Race | Finished",
                   large_image=str(getTrack()),
                   small_image=str(getCar()),
                   large_text="Track",
                   small_text=teamInCorrectFormat(getCar()))
    else:
        RPC.update(state=str(str(getPlayerPosition()) + "/" + str(getNumberOfDrivers())+" | "+getWeather()),
                   details="Race | " + str(getLapNumber()) + "/" + str(getTotalLapNumber()) + " laps",
                   large_image=str(getTrack()),
                   small_image=str(getCar()),
                   large_text="Track",
                   small_text=teamInCorrectFormat(getCar()))

def showQualiPresence(type):
    if (isUserSpectating() == True):
        RPC.update(state=str(type)+" | "+getWeather(),
                   details=str(("Spectating " + str(getNumberOfDrivers()) + " driver") if getNumberOfDrivers() == 1 else ("Spectating " + str(getNumberOfDrivers()) + " drivers")),
                   large_image=str(getTrack()),
                   large_text="Track")

    if(type=="OSQ"):
        RPC.update(state=str(getPlayerPosition()+" at this moment"),
                   details=type + " | " +getWeather(),
                   large_image=str(getTrack()),
                   small_image=str(getCar()),
                   large_text="Track",
                   small_text=teamInCorrectFormat(getCar()))

    else:
        RPC.update(state=str(getPlayerPosition() + "/" + str(getNumberOfDrivers())+" | "+getWeather()),
                   details= type+" | Best lap: " +str(getBestLap()),
                   large_image=str(getTrack()),
                   small_image= str(getCar()),
                   large_text="Track",
                   small_text=teamInCorrectFormat(getCar()))
def showTimeTrialPresence():
    RPC.update(state="Weather: "+getWeather(),
               details= "Time Trial | "+str(getBestLap()),
               large_image = str(getTrack()),
               small_image= str(getCar()),
               large_text="Track",
               small_text=teamInCorrectFormat(getCar()))

def showPracticePresence(type):
    RPC.update(state="Weather: " + getWeather(),
               details=type +" | " +str(getBestLap()),
               large_image=str(getTrack()),
               small_image=str(getCar()),
               large_text="Track",
               small_text=teamInCorrectFormat(getCar()))

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
                showQualiPresence("SQ")
            elif (packet.sessionType == 9):
                showQualiPresence("OSQ")
            elif (packet.sessionType == 12):
                showTimeTrialPresence()
            elif (packet.sessionType == 1):
                showPracticePresence("P1")
            elif (packet.sessionType == 2):
                showTimeTrialPresence("P2")
            elif (packet.sessionType == 3):
                showTimeTrialPresence("P3")
            elif (packet.sessionType == 4):
                showTimeTrialPresence("Short Practice")
            else:
                RPC.update(large_image="f12020", details="Idling")

    except socket.timeout:
        RPC.update(large_image="f12020", details="Idling")
        while not "F1_2020_dx12.exe" in (p.name() for p in psutil.process_iter()):
            RPC.clear(os.getpid())
            continue






