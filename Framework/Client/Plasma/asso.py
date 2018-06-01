from ConfigParser import ConfigParser

from Utilities.Packet import Packet


def HandleGetAssociations(self, data):
    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TXN", "GetAssociations")

    type = data.get("PacketData", "type")
    newPacket.set("PacketData", "type", type)
    newPacket.set("PacketData", "domainPartition.domain", data.get("PacketData", "domainPartition.domain"))
    newPacket.set("PacketData", "domainPartition.subDomain", data.get("PacketData", "domainPartition.subDomain"))
    newPacket.set("PacketData", "owner.id", self.CONNOBJ.personaID)
    newPacket.set("PacketData", "owner.name", self.CONNOBJ.personaName)
    newPacket.set("PacketData", "owner.type", "1")

    if type == "PlasmaMute":
        # TODO: Make the mute list database
        newPacket.set("PacketData", "maxListSize", "20")
        newPacket.set("PacketData", "members.[]", "0")
    elif type == 'PlasmaBlock':
        # TODO: Make the block list database
        newPacket.set("PacketData", "maxListSize", "20")
        newPacket.set("PacketData", "members.[]", "0")
    elif type == 'PlasmaFriends':
        # TODO: Make the friends list database
        newPacket.set("PacketData", "maxListSize", "20")
        newPacket.set("PacketData", "members.[]", "0")
    elif type == 'PlasmaRecentPlayers':
        # TODO: Make the recent list database
        newPacket.set("PacketData", "maxListSize", "100")
        newPacket.set("PacketData", "members.[]", "0")

    Packet(newPacket).sendPacket(self, "asso", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == "GetAssociations":
        HandleGetAssociations(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown asso message (' + txn + ")", 2)
