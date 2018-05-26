from threading import Timer

from ConfigParser import ConfigParser

from Logger import Log
from Utilities.Packet import Packet
from Utilities.RandomStringGenerator import GenerateRandomString

logger = Log("PlasmaClient", "\033[33;1m")


def SendMemCheck(self):
    newPacketData = ConfigParser()
    newPacketData.optionxform = str

    newPacketData.add_section("PacketData")

    newPacketData.set("PacketData", "TXN", "MemCheck")
    newPacketData.set("PacketData", "memcheck.[]", 0)
    newPacketData.set("PacketData", "type", 0)
    newPacketData.set("PacketData", "salt", GenerateRandomString(9))

    newPacket = Packet(newPacketData).generatePacket("fsys", 0x80000000, 0)

    if self.CONNOBJ.IsUp:
        self.transport.getHandle().sendall(newPacket)
        logger.new_message("[" + self.ip + ":" + str(self.port) + ']--> ' + repr(newPacket), 3)
        logger.new_message("[" + self.ip + ":" + str(self.port) + '][fsys] Sent MemCheck to client!', 2)


def ReceiveMemCheck(self):
    memcheck_timer = Timer(300, SendMemCheck, [self, ])  # Send MemCheck after 300 second from last MemCheck result
    memcheck_timer.start()
