from ConfigParser import ConfigParser

from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    """ Create Game """

    toSend = Packet().create()
    toSend.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))

    self.CONNOBJ.serverData = ConfigParser()
    self.CONNOBJ.serverData.optionxform = str
    self.CONNOBJ.serverData.add_section("ServerData")

    for item in data.items("PacketData"):
        if item[0] != "TID":
            self.CONNOBJ.serverData.set("ServerData", item[0], str(item[1]).replace('"', ""))

    toSend.set("PacketData", "MAX-PLAYERS", str(data.get("PacketData", "MAX-PLAYERS")))
    toSend.set("PacketData", "EKEY", "AIBSgPFqRDg0TfdXW1zUGa4%3d")
    toSend.set("PacketData", "UGID", str(data.get("PacketData", "UGID")))
    toSend.set("PacketData", "JOIN", str(data.get("PacketData", "JOIN")))

    if len(data.get("PacketData", "SECRET")) != 0:
        toSend.set("PacketData", "SECRET", data.get("PacketData", "SECRET"))
    else:
        toSend.set("PacketData", "SECRET", "4l94N6Y0A3Il3+kb55pVfK6xRjc+Z6sGNuztPeNGwN5CMwC7ZlE/lwel07yciyZ5y3bav7whbzHugPm11NfuBg%3d%3d")

    toSend.set("PacketData", "LID", "1")
    toSend.set("PacketData", "J", str(data.get("PacketData", "JOIN")))
    toSend.set("PacketData", "GID", str(self.CONNOBJ.GameID))

    Packet(toSend).send(self, "CGAM", 0x00000000, 0)

    self.logger.new_message("[" + self.ip + ":" + str(self.port) + "] Created new game!", 1)
