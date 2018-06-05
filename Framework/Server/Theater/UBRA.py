from Utilities.Packet import Packet


def ReceivePacket(self, data):

    if data.get("PacketData", "START") == "1":
        self.CONNOBJ.startedUBRAs += 2
    else:
        orig_tid = int(data.get("PacketData", "TID")) - self.CONNOBJ.startedUBRAs / 2

        for packet in range(self.CONNOBJ.startedUBRAs):
            toSend = Packet().create()
            toSend.set("PacketData", "TID", str(orig_tid + packet))

            Packet(toSend).send(self, "UBRA", 0x00000000, 0)
            self.CONNOBJ.startedUBRAs -= 1
