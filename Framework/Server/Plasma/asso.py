from Utilities.Packet import Packet


def HandleGetAssociations(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "GetAssociations")

    type = data.get("PacketData", "type")

    toSend.set("PacketData", "domainPartition.domain", data.get("PacketData", "domainPartition.domain"))
    toSend.set("PacketData", "domainPartition.subDomain", data.get("PacketData", "domainPartition.subDomain"))
    toSend.set("PacketData", "owner.id", str(self.CONNOBJ.personaID))
    toSend.set("PacketData", "owner.type", "1")
    toSend.set("PacketData", "type", type)
    toSend.set("PacketData", "members.[]", "0")

    if type == "PlasmaMute":
        toSend.set("PacketData", "maxListSize", "20")
        toSend.set("PacketData", "owner.name", self.CONNOBJ.personaName)
    elif type == 'PlasmaBlock':
        toSend.set("PacketData", "maxListSize", "20")
        toSend.set("PacketData", "owner.name", self.CONNOBJ.personaName)
    elif type == 'PlasmaFriends':
        toSend.set("PacketData", "maxListSize", "20")
        toSend.set("PacketData", "owner.name", self.CONNOBJ.personaName)
    elif type == 'PlasmaRecentPlayers':
        toSend.set("PacketData", "maxListSize", "100")
    elif type == 'dogtags':
        toSend.set("PacketData", "maxListSize", "20")
        toSend.set("PacketData", "owner.name", self.CONNOBJ.personaName)

    Packet(toSend).send(self, "asso", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleAddAssociations(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "AddAssociations")

    type = data.get("PacketData", "type")

    toSend.set("PacketData", "domainPartition.domain", data.get("PacketData", "domainPartition.domain"))
    toSend.set("PacketData", "domainPartition.subDomain", data.get("PacketData", "domainPartition.subDomain"))
    toSend.set("PacketData", "type", type)
    toSend.set("PacketData", "result.[]", "0")

    if type == 'PlasmaRecentPlayers':
        toSend.set("PacketData", "maxListSize", "100")

    Packet(toSend).send(self, "asso", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == "GetAssociations":
        HandleGetAssociations(self, data)
    elif txn == "AddAssociations":
        HandleAddAssociations(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown asso message (' + txn + ")", 2)
