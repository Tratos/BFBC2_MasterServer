from ConfigParser import ConfigParser

from Globals import Servers
from Utilities.Packet import Packet
from Utilities.RandomStringGenerator import GenerateRandomString


def ReceiveRequest(self, data):
    self.logger.new_message("[" + self.ip + ":" + str(self.port) + "] wants to join server", 1)

    lid = data.get("PacketData", "LID")
    gid = data.get("PacketData", "GID")

    newEGAMPacket = ConfigParser()
    newEGAMPacket.optionxform = str
    newEGAMPacket.add_section("PacketData")
    newEGAMPacket.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
    newEGAMPacket.set("PacketData", "LID", str(lid))
    newEGAMPacket.set("PacketData", "GID", str(gid))


    serverPID = 0
    serverData = None
    serverIpAddr = None
    serverSocket = None
    for server in Servers:
        if server.serverData.get("ServerData", "GID") == str(gid):
            serverPID = server.personaID
            serverData = server.serverData
            serverIpAddr = server.ipAddr
            serverSocket = server.theaterInt
            break

    if serverSocket is not None:
        """ This packet gets sent to the SERVER the client connects to, it contains information about the client """

        ticket = GenerateRandomString(10)

        newPacket = ConfigParser()
        newPacket.optionxform = str
        newPacket.add_section("PacketData")
        newPacket.set("PacketData", "R-INT-PORT", str(data.get("PacketData", "R-INT-PORT")))
        newPacket.set("PacketData", "R-INT-IP", str(data.get("PacketData", "R-INT-IP")))  # internal ip where the CLIENT is hosted
        newPacket.set("PacketData", "PORT", str(data.get("PacketData", "PORT")))
        newPacket.set("PacketData", "NAME", self.CONNOBJ.personaName)
        newPacket.set("PacketData", "PTYPE", str(data.get("PacketData", "PTYPE")))
        newPacket.set("PacketData", "TICKET", ticket)
        newPacket.set("PacketData", "PID", "1")
        newPacket.set("PacketData", "UID", str(self.CONNOBJ.personaID))

        if self.CONNOBJ.ipAddr[0] == serverIpAddr[0]:  # Client and Server has the same ip?
            newPacket.set("PacketData", "IP", data.get("PacketData", "R-INT-IP"))
        else:
            newPacket.set("PacketData", "IP", self.CONNOBJ.ipAddr[0])  # Client and Server are in diffirent networks, so send public ip of client

        newPacket.set("PacketData", "LID", str(lid))
        newPacket.set("PacketData", "GID", str(gid))

        Packet(newPacket).sendPacket(serverSocket, "EGRQ", 0x00000000, 0)
        Packet(newEGAMPacket).sendPacket(self, "EGAM", 0x00000000, 0)

        newPacket = ConfigParser()
        newPacket.optionxform = str
        newPacket.add_section("PacketData")
        newPacket.set("PacketData", "PL", "pc")
        newPacket.set("PacketData", "TICKET", ticket)
        newPacket.set("PacketData", "PID", "1")

        if self.CONNOBJ.ipAddr[0] == serverIpAddr[0]:  # Client and Server has the same ip?
            newPacket.set("PacketData", "I", serverData.get("ServerData", "INT-IP"))
            newPacket.set("PacketData", "P", str(serverData.get("ServerData", "INT-PORT")))  # Port
        else:
            newPacket.set("PacketData", "I", serverIpAddr[0])  # Client and Server are in diffirent networks, so send public ip of server
            newPacket.set("PacketData", "P", str(serverData.get("ServerData", "PORT")))  # Port

        newPacket.set("PacketData", "HUID", str(serverPID))
        newPacket.set("PacketData", "INT-PORT", str(serverData.get("ServerData", "INT-PORT")))  # Port
        newPacket.set("PacketData", "EKEY", "AIBSgPFqRDg0TfdXW1zUGa4%3d")  # this must be the same key as the one we have on the server? keep it constant in both connections for now (we could integrate it in the database...)
        newPacket.set("PacketData", "INT-IP", serverData.get("ServerData", "INT-IP"))  # internal ip where the SERVER is hosted
        newPacket.set("PacketData", "UGID", serverData.get("ServerData", "UGID"))
        newPacket.set("PacketData", "LID", str(lid))
        newPacket.set("PacketData", "GID", str(gid))

        Packet(newPacket).sendPacket(self, "EGEG", 0x00000000, 0)
