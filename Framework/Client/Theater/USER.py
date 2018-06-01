from ConfigParser import ConfigParser

from Globals import Clients

from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    newPacketData = ConfigParser()
    newPacketData.optionxform = str
    newPacketData.add_section("PacketData")

    lkey = data.get("PacketData", "LKEY")

    for client in Clients:
        if client.personaSessionKey == lkey:
            self.CONNOBJ = client
            self.CONNOBJ.theaterPacketID = int(data.get("PacketData", "TID"))

    if self.CONNOBJ is None:
        self.transport.loseConnection()
    else:
        newPacketData.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
        newPacketData.set("PacketData", "NAME", self.CONNOBJ.personaName)

        Packet(newPacketData).sendPacket(self, "USER", 0x00000000, 0)
        self.CONNOBJ.theaterPacketID += 1
