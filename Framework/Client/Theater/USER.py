from Globals import Clients

from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    toSend = Packet().create()

    lkey = data.get("PacketData", "LKEY")

    for client in Clients:
        if client.personaSessionKey == lkey:
            self.CONNOBJ = client
            self.CONNOBJ.theaterPacketID = int(data.get("PacketData", "TID"))

    if self.CONNOBJ is None:
        self.transport.loseConnection()
    else:
        toSend.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
        toSend.set("PacketData", "NAME", self.CONNOBJ.personaName)

        Packet(toSend).send(self, "USER", 0x00000000, 0)
