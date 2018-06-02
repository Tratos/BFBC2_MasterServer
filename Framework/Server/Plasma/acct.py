# -*- coding: utf-8 -*-

from base64 import b64encode, b64decode

from ConfigParser import ConfigParser

from Database import Database
from Utilities.Packet import Packet
from Utilities.RandomStringGenerator import GenerateRandomString

db = Database()


def HandleNuLogin(self, data):
    validServers = {'bfbc2.server.pc@ea.com': 'Che6rEPA',
                    'bfbc.server.ps3@ea.com': 'zAmeH7bR',
                    'bfbc.server.xenon@ea.com': 'B8ApRavE'}

    loginResult = ConfigParser()
    loginResult.optionxform = str
    loginResult.add_section("PacketData")
    loginResult.set("PacketData", "TXN", "NuLogin")

    returnEncryptedInfo = int(
        data.get("PacketData", "returnEncryptedInfo"))  # If 1 - User wants to store login information

    try:
        nuid = data.get('PacketData', "nuid")
        password = data.get('PacketData', "password")
    except:
        encryptedInfo = data.get("PacketData", "encryptedInfo")

        encryptedLoginData = encryptedInfo.replace("Ciyvab0tregdVsBtboIpeChe4G6uzC1v5_-SIxmvSL", "")
        encryptedLoginData = encryptedLoginData.replace("-", "=").replace("_",
                                                                          "=")  # Bring string into proper format again

        loginData = b64decode(encryptedLoginData).split('\f')

        nuid = loginData[0]
        password = loginData[1]

    try:
        serverPassword = validServers[nuid]

        if serverPassword == password:
            loginStatus = True
        else:
            loginStatus = "INCORRECT_PASSWORD"
    except:
        self.logger_err.new_message("[Login] Server wanted to login with incorrect login data!", 1)
        loginStatus = False

    if loginStatus:
        self.CONNOBJ.accountSessionKey = db.registerSession()

        if nuid == "bfbc2.server.pc@ea.com":
            self.CONNOBJ.userID = 1
        elif nuid == "bfbc.server.ps3@ea.com":
            self.CONNOBJ.userID = 2
        elif nuid == "bfbc.server.xenon@ea.com":
            self.CONNOBJ.userID = 3
        else:
            self.CONNOBJ.userID = -1

        self.CONNOBJ.nuid = nuid

        loginResult.set("PacketData", "lkey", self.CONNOBJ.accountSessionKey)
        loginResult.set("PacketData", "nuid", nuid)

        if returnEncryptedInfo == 1:
            encryptedLoginData = "Ciyvab0tregdVsBtboIpeChe4G6uzC1v5_-SIxmvSL"
            encryptedLoginData += GenerateRandomString(86)

            loginResult.set("PacketData", "encryptedLoginInfo", encryptedLoginData)

        loginResult.set("PacketData", "profileId", str(self.CONNOBJ.userID))
        loginResult.set("PacketData", "userId", str(self.CONNOBJ.userID))

        self.logger.new_message("[Login] Server " + nuid + " logged in successfully!", 1)
    elif loginStatus == "INCORRECT_PASSWORD":  # The password the user specified is incorrect
        loginResult.set("PacketData", "localizedMessage", "The password the user specified is incorrect")
        loginResult.set("PacketData", "errorContainer.[]", "0")
        loginResult.set("PacketData", "errorCode", "122")

        self.logger_err.new_message("[Login] Server " + nuid + " specified incorrect password!", 1)
    else:  # User not found
        loginResult.set("PacketData", "localizedMessage", "The user was not found")
        loginResult.set("PacketData", "errorContainer.[]", "0")
        loginResult.set("PacketData", "errorCode", "101")

        self.logger_err.new_message("[Login] Server " + nuid + " does not exist", 1)

    Packet(loginResult).sendPacket(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuGetPersonas(self):
    """ Get personas associated with account """

    userID = self.CONNOBJ.userID

    personaList = ConfigParser()
    personaList.optionxform = str
    personaList.add_section("PacketData")
    personaList.set("PacketData", "TXN", "NuGetPersonas")
    personaList.set("PacketData", "personas.[]", "1")

    if userID == 1:
        personaList.set("PacketData", "personas.0", "bfbc2.server.p")
    elif userID == 2:
        personaList.set("PacketData", "personas.0", "bfbc.server.ps")
    elif userID == 3:
        personaList.set("PacketData", "personas.0", "bfbc.server.xe")

    Packet(personaList).sendPacket(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuLoginPersona(self, data):
    personaLoginResult = ConfigParser()
    personaLoginResult.optionxform = str
    personaLoginResult.add_section("PacketData")
    personaLoginResult.set("PacketData", "TXN", "NuLoginPersona")

    requestedPersonaName = data.get("PacketData", "name")

    if requestedPersonaName in self.CONNOBJ.validPersonas:
        self.CONNOBJ.personaID = self.CONNOBJ.validPersonas[requestedPersonaName]
        self.CONNOBJ.personaSessionKey = db.registerSession()
        self.CONNOBJ.personaName = requestedPersonaName

        personaLoginResult.set("PacketData", "lkey", self.CONNOBJ.personaSessionKey)
        personaLoginResult.set("PacketData", "profileId", str(self.CONNOBJ.personaID))
        personaLoginResult.set("PacketData", "userId", str(self.CONNOBJ.personaID))

        self.logger.new_message("[Persona] Server " + self.CONNOBJ.nuid + " just logged as " + requestedPersonaName, 1)
    else:
        personaLoginResult.set("PacketData", "localizedMessage", "The user was not found")
        personaLoginResult.set("PacketData", "errorContainer.[]", "0")
        personaLoginResult.set("PacketData", "errorCode", "101")
        self.logger_err.new_message(
            "[Persona] Server " + self.CONNOBJ.nuid + " wanted to login as " + requestedPersonaName + " but this persona cannot be found!",
            1)

    Packet(personaLoginResult).sendPacket(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuGetEntitlements(self, data):
    groupName = data.get("PacketData", "groupName")

    # TODO: Make the BFBC2 entitlements database

    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TXN", "NuGetEntitlements")
    newPacket.set("PacketData", "entitlements.[]", "0")

    Packet(newPacket).sendPacket(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'NuLogin':
        HandleNuLogin(self, data)
    elif txn == 'NuGetPersonas':
        HandleNuGetPersonas(self)
    elif txn == 'NuLoginPersona':
        HandleNuLoginPersona(self, data)
    elif txn == 'NuGetEntitlements':
        HandleNuGetEntitlements(self, data)
    else:
        self.logger_err.new_message(
            "[" + self.ip + ":" + str(self.port) + ']<-- Got unknown acct message (' + txn + ")", 2)
