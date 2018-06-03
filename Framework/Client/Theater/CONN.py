from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    toSend = Packet().create()

    tid = data.get("PacketData", "TID")
    prot = data.get("PacketData", "PROT")

    toSend.set("PacketData", "TID", str(tid))
    toSend.set("PacketData", "TIME", "0")
    toSend.set("PacketData", "activityTimeoutSecs", "240")
    toSend.set("PacketData", "PROT", prot)

    Packet(toSend).send(self, "CONN", 0x00000000, 0)
