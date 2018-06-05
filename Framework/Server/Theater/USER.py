from Globals import Servers

from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    toSend = Packet().create()

    lkey = data.get("PacketData", "LKEY")

    for server in Servers:
        if server.personaSessionKey == lkey:
            self.CONNOBJ = server
            self.CONNOBJ.theaterPacketID = int(data.get("PacketData", "TID"))
            self.CONNOBJ.theaterInt = self

    if self.CONNOBJ is None:
        self.transport.loseConnection()
    else:
        toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
        toSend.set("PacketData", "NAME", self.CONNOBJ.personaName)

        Packet(toSend).send(self, "USER", 0x00000000, 0)
