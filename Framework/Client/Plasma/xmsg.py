from Database import Database
from Utilities.Packet import Packet

db = Database()


def HandleModifySettings(self):
    # TODO: Modify settings in database

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "ModifySettings")

    Packet(toSend).send(self, "xmsg", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleGetMessages(self):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "GetMessages")

    userMessages = db.getMessages(self.CONNOBJ.personaID)

    if len(userMessages) != 0:
        count = 0
        for message in userMessages:

            attachmentsDB = message['attachments'].split("|")
            attachmentCount = len(attachmentsDB) - 2  # Remove beginning and ending

            curMsg = 1
            attachments = []
            for attachment in range(attachmentCount):
                attachments.append(attachmentsDB[curMsg].split(":"))
                curMsg += 2

            attachmentCount = 0
            for attachment in attachments:
                toSend.set("PacketData", "messages." + str(count) + ".attachments." + str(attachmentCount) + ".type", str(attachment[0]))
                toSend.set("PacketData", "messages." + str(count) + ".attachments." + str(attachmentCount) + ".key", str(attachment[1]))
                toSend.set("PacketData", "messages." + str(count) + ".attachments." + str(attachmentCount) + ".data", '"' + str(attachment[2]) + '"')
                attachmentCount += 1

            toSend.set("PacketData", "messages." + str(count) + ".attachments.[]", str(attachmentCount))

            toSend.set("PacketData", "messages." + str(count) + ".messageId", message['messageID'])
            toSend.set("PacketData", "messages." + str(count) + ".from.name", message['senderPersonaName'])
            toSend.set("PacketData", "messages." + str(count) + ".from.id", message['senderID'])

            toSend.set("PacketData", "messages." + str(count) + ".messageType", message['messageType'])
            toSend.set("PacketData", "messages." + str(count) + ".deliveryType", message['deliveryType'])
            toSend.set("PacketData", "messages." + str(count) + ".purgeStrategy", message['purgeStrategy'])
            toSend.set("PacketData", "messages." + str(count) + ".expiration", message['expiration'])
            toSend.set("PacketData", "messages." + str(count) + ".timeSent", message['timeSent'])

            #  Unknown things (why this are being send by original server?)
            toSend.set("PacketData", "messages." + str(count) + ".to.0.name", str(self.CONNOBJ.personaName))
            toSend.set("PacketData", "messages." + str(count) + ".to.0.id", str(self.CONNOBJ.personaID))
            toSend.set("PacketData", "messages." + str(count) + ".to.[]", "1")

            count += 1

    toSend.set("PacketData", "messages.[]", str(len(userMessages)))

    Packet(toSend).send(self, "xmsg", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleSendMessage(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "SendMessage")

    to = int(data.get("PacketData", "to.[]"))
    attachmentsCount = int(data.get("PacketData", "attachments.[]"))

    attachments = ""
    toUsers = []

    for i in range(to):
        toUsers.append(int(data.get("PacketData", "to." + str(i))))

    for i in range(attachmentsCount):
        attachments += "|" + data.get("PacketData", "attachments." + str(i) + ".type") + ":" + data.get("PacketData", "attachments." + str(i) + ".key") + ":" + data.get("PacketData", "attachments." + str(i) + ".data") + "|"

    messageId = db.sendMessage(self.CONNOBJ.personaID, toUsers, data.get("PacketData", "messageType"), attachments, int(data.get("PacketData", "expires")), data.get("PacketData", "deliveryType"), data.get("PacketData", "purgeStrategy"))

    if messageId is not False:
        toSend.set('PacketData', 'messageId', str(messageId))
        toSend.set("PacketData", "status.[]", str(len(toUsers)))

        count = 0

        for user in toUsers:
            toSend.set("PacketData", "status." + str(count) + ".status", "1")
            toSend.set("PacketData", "status." + str(count) + ".userid", str(user))
    else:
        toSend.set('PacketData', 'messageId', "0")
        toSend.set("PacketData", "status.[]", str(len(toUsers)))

        count = 0

        for user in toUsers:
            toSend.set("PacketData", "status." + str(count) + ".status", "0")
            toSend.set("PacketData", "status." + str(count) + ".userid", str(user))

    Packet(toSend).send(self, "xmsg", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleDeleteMessages(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "DeleteMessages")

    messagesToDelete = int(data.get("PacketData", "messageIds.[]"))
    messageIds = []

    for message in range(messagesToDelete):
        messageIds.append(data.get("PacketData", "messageIds." + str(message)))

    db.deleteMessages(messageIds)

    Packet(toSend).send(self, "xmsg", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'ModifySettings':
        HandleModifySettings(self)
    elif txn == 'GetMessages':
        HandleGetMessages(self)
    elif txn == 'SendMessage':
        HandleSendMessage(self, data)
    elif txn == 'DeleteMessages':
        HandleDeleteMessages(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown xmsg message (' + txn + ")", 2)
