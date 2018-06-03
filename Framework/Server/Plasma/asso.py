from Utilities.Packet import Packet


def HandleGetAssociations(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "GetAssociations")

    type = data.get("PacketData", "type")
    toSend.set("PacketData", "type", type)
    toSend.set("PacketData", "domainPartition.domain", data.get("PacketData", "domainPartition.domain"))
    toSend.set("PacketData", "domainPartition.subDomain", data.get("PacketData", "domainPartition.subDomain"))
    toSend.set("PacketData", "owner.id", str(self.CONNOBJ.personaID))
    toSend.set("PacketData", "owner.name", self.CONNOBJ.personaName)
    toSend.set("PacketData", "owner.type", "1")

    if type == "PlasmaMute":
        # TODO: Make the mute list database
        toSend.set("PacketData", "maxListSize", "20")
        toSend.set("PacketData", "members.[]", "0")
    elif type == 'PlasmaBlock':
        # TODO: Make the block list database
        toSend.set("PacketData", "maxListSize", "20")
        toSend.set("PacketData", "members.[]", "0")
    elif type == 'PlasmaFriends':
        # TODO: Make the friends list database
        toSend.set("PacketData", "maxListSize", "20")
        toSend.set("PacketData", "members.[]", "0")
    elif type == 'PlasmaRecentPlayers':
        # TODO: Make the recent list database
        toSend.set("PacketData", "maxListSize", "100")
        toSend.set("PacketData", "members.[]", "0")

    Packet(toSend).send(self, "asso", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == "GetAssociations":
        HandleGetAssociations(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown asso message (' + txn + ")", 2)
