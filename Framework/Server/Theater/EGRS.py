from Utilities.Packet import Packet


def ReceivePacket(self, data):
    toSend = Packet().create()

    allowed = data.get("PacketData", "ALLOWED")

    if str(allowed) == "1":
        # TODO: Add player to JOINING_PLAYERS
        pass

    toSend.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
    Packet(toSend).send(self, "EGRS", 0x00000000, 0)
