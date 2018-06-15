from Globals import Clients

from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    toSend = Packet().create()

    lkey = data.get("PacketData", "LKEY")

    for client in Clients:
        if client.personaSessionKey == lkey:
            self.CONNOBJ = client

    if self.CONNOBJ is None:
        self.transport.loseConnection()
    else:
        toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
        toSend.set("PacketData", "NAME", self.CONNOBJ.personaName)

        Packet(toSend).send(self, "USER", 0x00000000, 0)
