from Database import Database
from Utilities.Packet import Packet

db = Database()


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
        associations = db.getUserAssociations(self.CONNOBJ.userID, 'MutedPlayers')
    elif type == 'PlasmaBlock':
        associations = db.getUserAssociations(self.CONNOBJ.userID, 'BlockedPlayers')
    elif type == 'PlasmaFriends':
        associations = db.getUserAssociations(self.CONNOBJ.userID, 'UsersFriends')
    elif type == 'PlasmaRecentPlayers':
        associations = db.getUserAssociations(self.CONNOBJ.userID, 'RecentPlayers')
    else:
        associations = []

    if len(associations) > 0:
        toSend.set("PacketData", "maxListSize", str(100 * (len(associations) / 2)))
    else:
        toSend.set("PacketData", "maxListSize", "100")

    count = 0
    for association in associations:
        toSend.set("PacketData", "members." + str(count) + ".id", association['concernUserID'])
        toSend.set("PacketData", "members." + str(count) + ".name", association['concernPersonaName'])
        toSend.set("PacketData", "members." + str(count) + ".type", association['type'])
        toSend.set("PacketData", "members." + str(count) + ".created", association['creationDate'])
        toSend.set("PacketData", "members." + str(count) + ".modified", association['creationDate'])
    toSend.set("PacketData", "members.[]", str(len(associations)))

    Packet(toSend).send(self, "asso", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == "GetAssociations":
        HandleGetAssociations(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown asso message (' + txn + ")", 2)
