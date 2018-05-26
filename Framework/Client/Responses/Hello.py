from time import strftime

from ConfigParser import ConfigParser

from Config import readFromConfig
from Logger import Log
from Utilities.Packet import Packet
from Utilities.RandomStringGenerator import GenerateRandomString

logger = Log("PlasmaClient", "\033[33;1m")


def SaveData(self, data):
    self.CONNOBJ.clientString = data.get("PacketData", "clientString")
    self.CONNOBJ.sku = data.get("PacketData", "sku")
    self.CONNOBJ.locale = data.get("PacketData", "locale")
    self.CONNOBJ.clientString = data.get("PacketData", "clientString")
    self.CONNOBJ.clientVersion = data.get("PacketData", "clientVersion")
    self.CONNOBJ.SDKVersion = data.get("PacketData", "SDKVersion")
    self.CONNOBJ.protocolVersion = data.get("PacketData", "protocolVersion")
    self.CONNOBJ.fragmentSize = data.get("PacketData", "fragmentSize")
    self.CONNOBJ.clientType = data.get("PacketData", "clientType")


def Hello(self, data):
    SaveData(self, data)

    currentTime = strftime('%b-%d-%Y %H:%M:%S UTC')

    newPacketData = ConfigParser()
    newPacketData.optionxform = str

    newPacketData.add_section("PacketData")

    newPacketData.set("PacketData", "domainPartition.domain", "eagames")
    newPacketData.set("PacketData", "messengerIp", readFromConfig("connection", "emulator_ip"))
    newPacketData.set("PacketData", "messengerPort", 0)  # Unknown data are being send to this port
    newPacketData.set("PacketData", "domainPartition.subDomain", "BFBC2")
    newPacketData.set("PacketData", "TXN", "Hello")
    newPacketData.set("PacketData", "activityTimeoutSecs", 0)  # We could let idle clients disconnect here automatically?
    newPacketData.set("PacketData", "curTime", currentTime)
    newPacketData.set("PacketData", "theaterIp", readFromConfig("connection", "emulator_ip"))
    newPacketData.set("PacketData", "theaterPort", readFromConfig("connection", "theater_client_port"))

    newPacket = Packet(newPacketData).generatePacket("fsys", 0x80000000, self.CONNOBJ.plasmaPacketID)

    self.transport.getHandle().sendall(newPacket)
    logger.new_message("[" + self.ip + ":" + str(self.port) + ']--> ' + repr(newPacket), 2)

    newPacketData = ConfigParser()
    newPacketData.optionxform = str

    newPacketData.add_section("PacketData")

    newPacketData.set("PacketData", "TXN", "MemCheck")
    newPacketData.set("PacketData", "memcheck.[]", 0)
    newPacketData.set("PacketData", "type", 0)
    newPacketData.set("PacketData", "salt", GenerateRandomString(9))

    newPacket = Packet(newPacketData).generatePacket("fsys", 0x80000000, 0)

    self.transport.getHandle().sendall(newPacket)
    logger.new_message("[" + self.ip + ":" + str(self.port) + ']--> ' + repr(newPacket), 2)
