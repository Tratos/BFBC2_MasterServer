from Globals import Servers
from Utilities.Packet import Packet
from Utilities.RandomStringGenerator import GenerateRandomString


def ReceiveRequest(self, data):
    self.logger.new_message("[" + self.ip + ":" + str(self.port) + "] wants to join server", 1)

    lid = data.get("PacketData", "LID")
    gid = data.get("PacketData", "GID")

    toSendEGAM = Packet().create()
    toSendEGAM.set("PacketData", "TID", str(data.get("PacketData", "TID")))
    toSendEGAM.set("PacketData", "LID", str(lid))
    toSendEGAM.set("PacketData", "GID", str(gid))

    server = None
    for tempServer in Servers:
        if tempServer.serverData.get("ServerData", "GID") == str(gid):
            tempServer.newPlayerID += 1
            server = tempServer
            break

    if server is not None:
        """ This packet gets sent to the SERVER the client connects to, it contains information about the client """

        self.CONNOBJ.playerID = server.newPlayerID
        server.connectedPlayers.append(self.CONNOBJ)

        ticket = GenerateRandomString(10)

        toSend = Packet().create()
        toSend.set("PacketData", "R-INT-PORT", str(data.get("PacketData", "R-INT-PORT")))
        toSend.set("PacketData", "R-INT-IP", str(data.get("PacketData", "R-INT-IP")))  # internal ip where the CLIENT is hosted
        toSend.set("PacketData", "PORT", str(data.get("PacketData", "PORT")))
        toSend.set("PacketData", "NAME", self.CONNOBJ.personaName)
        toSend.set("PacketData", "PTYPE", str(data.get("PacketData", "PTYPE")))
        toSend.set("PacketData", "TICKET", ticket)
        toSend.set("PacketData", "PID", str(self.CONNOBJ.playerID))
        toSend.set("PacketData", "UID", str(self.CONNOBJ.personaID))
        toSend.set("PacketData", "IP", self.CONNOBJ.ipAddr)

        toSend.set("PacketData", "LID", str(lid))
        toSend.set("PacketData", "GID", str(gid))

        Packet(toSend).send(server.theaterInt, "EGRQ", 0x00000000, 0)
        Packet(toSendEGAM).send(self, "EGAM", 0x00000000, 0)

        toSend = Packet().create()
        toSend.set("PacketData", "PL", "pc")
        toSend.set("PacketData", "TICKET", ticket)
        toSend.set("PacketData", "PID", str(self.CONNOBJ.playerID))

        toSend.set("PacketData", "I", server.ipAddr)
        toSend.set("PacketData", "P", str(server.serverData.get("ServerData", "PORT")))  # Port

        toSend.set("PacketData", "HUID", str(server.personaID))
        toSend.set("PacketData", "INT-PORT", str(server.serverData.get("ServerData", "INT-PORT")))  # Port
        toSend.set("PacketData", "EKEY", "AIBSgPFqRDg0TfdXW1zUGa4%3d")  # this must be the same key as the one we have on the server? keep it constant in both connections for now (we could integrate it in the database...)
        toSend.set("PacketData", "INT-IP", server.serverData.get("ServerData", "INT-IP"))  # internal ip where the SERVER is hosted
        toSend.set("PacketData", "UGID", server.serverData.get("ServerData", "UGID"))
        toSend.set("PacketData", "LID", str(lid))
        toSend.set("PacketData", "GID", str(gid))

        Packet(toSend).send(self, "EGEG", 0x00000000, 0)
