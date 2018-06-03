# -*- coding: utf-8 -*-

from base64 import b64decode

from Database import Database
from Utilities.Packet import Packet
from Utilities.RandomStringGenerator import GenerateRandomString

db = Database()


def HandleNuLogin(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuLogin")

    returnEncryptedInfo = int(data.get("PacketData", "returnEncryptedInfo"))  # If 1 - User wants to store login information

    try:
        nuid = data.get('PacketData', "nuid")
        password = data.get('PacketData', "password")
    except:
        encryptedInfo = data.get("PacketData", "encryptedInfo")

        encryptedLoginData = encryptedInfo.replace("Ciyvab0tregdVsBtboIpeChe4G6uzC1v5_-SIxmvSL", "")
        encryptedLoginData = encryptedLoginData.replace("-", "=").replace("_", "=")  # Bring string into proper format again

        loginData = b64decode(encryptedLoginData).split('\f')

        nuid = loginData[0]
        password = loginData[1]

    try:
        serverPassword = self.CONNOBJ.validServers[nuid]['password']

        if serverPassword == password:
            loginStatus = True
        else:
            loginStatus = "INCORRECT_PASSWORD"
    except:
        self.logger_err.new_message("[Login] Server wanted to login with incorrect login data!", 1)
        loginStatus = False

    if loginStatus:
        self.CONNOBJ.accountSessionKey = db.registerSession()
        self.CONNOBJ.userID = self.CONNOBJ.validServers[nuid]['id']
        self.CONNOBJ.nuid = nuid

        toSend.set("PacketData", "lkey", self.CONNOBJ.accountSessionKey)
        toSend.set("PacketData", "nuid", nuid)

        if returnEncryptedInfo == 1:
            encryptedLoginData = "Ciyvab0tregdVsBtboIpeChe4G6uzC1v5_-SIxmvSL"
            encryptedLoginData += GenerateRandomString(86)

            toSend.set("PacketData", "encryptedLoginInfo", encryptedLoginData)

        toSend.set("PacketData", "profileId", str(self.CONNOBJ.userID))
        toSend.set("PacketData", "userId", str(self.CONNOBJ.userID))

        self.logger.new_message("[Login] Server " + nuid + " logged in successfully!", 1)
    elif loginStatus == "INCORRECT_PASSWORD":  # The password the user specified is incorrect
        toSend.set("PacketData", "localizedMessage", "The password the user specified is incorrect")
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "122")

        self.logger_err.new_message("[Login] Server " + nuid + " specified incorrect password!", 1)
    else:  # User not found
        toSend.set("PacketData", "localizedMessage", "The user was not found")
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "101")

        self.logger_err.new_message("[Login] Server " + nuid + " does not exist", 1)

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuGetPersonas(self):
    """ Get personas associated with account """

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuGetPersonas")
    toSend.set("PacketData", "personas.[]", "1")

    userID = self.CONNOBJ.userID

    if userID == 1:
        toSend.set("PacketData", "personas.0", "bfbc2.server.p")
    elif userID == 2:
        toSend.set("PacketData", "personas.0", "bfbc.server.ps")
    elif userID == 3:
        toSend.set("PacketData", "personas.0", "bfbc.server.xe")

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuLoginPersona(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuLoginPersona")

    requestedPersonaName = data.get("PacketData", "name")

    if requestedPersonaName in self.CONNOBJ.validPersonas:
        self.CONNOBJ.personaID = self.CONNOBJ.validPersonas[requestedPersonaName]
        self.CONNOBJ.personaSessionKey = db.registerSession()
        self.CONNOBJ.personaName = requestedPersonaName

        toSend.set("PacketData", "lkey", self.CONNOBJ.personaSessionKey)
        toSend.set("PacketData", "profileId", str(self.CONNOBJ.personaID))
        toSend.set("PacketData", "userId", str(self.CONNOBJ.personaID))

        self.logger.new_message("[Persona] Server " + self.CONNOBJ.nuid + " just logged as " + requestedPersonaName, 1)
    else:
        toSend.set("PacketData", "localizedMessage", "The user was not found")
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "101")
        self.logger_err.new_message("[Persona] Server " + self.CONNOBJ.nuid + " wanted to login as " + requestedPersonaName + " but this persona cannot be found!", 1)

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuGetEntitlements(self, data):
    # TODO: Make the BFBC2 entitlements database

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuGetEntitlements")
    toSend.set("PacketData", "entitlements.[]", "0")

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuLookupUserInfo(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuLookupUserInfo")

    personaName = data.get("PacketData", "userInfo.0.userName")

    if personaName in self.CONNOBJ.validPersonas:
        toSend.set("PacketData", "userInfo.[]", "1")
        toSend.set("PacketData", "userInfo.0.userName", personaName)
        toSend.set("PacketData", "userInfo.0.namespace", "battlefield")
        toSend.set("PacketData", "userInfo.0.userId", str(self.CONNOBJ.validPersonas[personaName]))
        toSend.set("PacketData", "userInfo.0.masterUserId", str(self.CONNOBJ.validPersonas[personaName]))
    else:
        toSend.set("PacketData", "userInfo.[]", "1")
        toSend.set("PacketData", "userInfo.0.userName", personaName)

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'NuLogin':
        HandleNuLogin(self, data)
    elif txn == 'NuGetPersonas':
        HandleNuGetPersonas(self)
    elif txn == 'NuLoginPersona':
        HandleNuLoginPersona(self, data)
    elif txn == 'NuGetEntitlements':
        HandleNuGetEntitlements(self, data)
    elif txn == 'NuLookupUserInfo':
        HandleNuLookupUserInfo(self, data)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown acct message (' + txn + ")", 2)
