from Utilities.Packet import Packet


def ReceiveRequest(self, data, addr):
    toSend = Packet().create()

    toSend.set("PacketData", "TXN", "ECHO")
    toSend.set("PacketData", "IP", addr[0])
    toSend.set("PacketData", "PORT", str(addr[1]))
    toSend.set("PacketData", "ERR", "0")
    toSend.set("PacketData", "TYPE", "1")
    toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))

    Packet(toSend).send(self, "ECHO", 0x00000000, 0, addr)
