# -*- coding: utf-8 -*-

from base64 import b64encode, b64decode
from datetime import datetime
from os.path import exists

from Config import readFromConfig
from Database import Database
from Utilities.Packet import Packet

from urllib import quote

db = Database()


def HandleGetCountryList(self):
    """ User wants to create a new account """

    toSend = Packet().create()

    if exists("Data/countryLists/countryList_" + self.CONNOBJ.locale):
        with open("Data/countryLists/countryList_" + self.CONNOBJ.locale) as countryListFile:
            countryListData = countryListFile.readlines()
    else:
        with open("Data/countryLists/default") as countryListFile:
            countryListData = countryListFile.readlines()

    toSend.set("PacketData", "TXN", "GetCountryList")
    toSend.set("PacketData", "countryList.[]", str(len(countryListData)))

    countryId = 0
    for line in countryListData:
        toSend.set("PacketData", "countryList." + str(countryId) + ".ISOCode", line.split("=")[0])
        toSend.set("PacketData", "countryList." + str(countryId) + ".description", line.split("=")[1].replace('"', "").replace("\n", ""))
        countryId += 1

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuGetTos(self):
    """ Get Terms of Use """

    toSend = Packet().create()

    toSend.set("PacketData", "TXN", "NuGetTos")
    toSend.set("PacketData", "version", "20426_17.20426_17")

    if exists("Data/termsOfUse/termsOfUse_" + self.CONNOBJ.locale):
        with open("Data/termsOfUse/termsOfUse_" + self.CONNOBJ.locale) as termsOfUseFile:
            termsOfUse = termsOfUseFile.read()
    else:
        with open("Data/termsOfUse/default") as termsOfUseFile:
            termsOfUse = termsOfUseFile.read()

    termsOfUse = quote(termsOfUse, safe=" ,.'&/()?;®@§[]").replace("%3A", "%3a").replace("%0A", "%0a") + "%0a%0a%09Battlefield%3a Bad Company 2 Master Server Emulator by B1naryKill3r%0ahttps://github.com/B1naryKill3r/BFBC2_MasterServer"
    toSend.set("PacketData", "tos", termsOfUse)

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuAddAccount(self, data):
    """ Final add account request (with data like email, password...) """

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuAddAccount")

    nuid = data.get('PacketData', 'nuid')  # Email
    password = data.get('PacketData', 'password')  # Password

    bd_Day = data.get('PacketData', 'DOBDay')
    bd_Month = data.get('PacketData', 'DOBMonth')
    bd_Year = data.get('PacketData', 'DOBYear')
    birthday = datetime.strptime(bd_Day + " " + bd_Month + " " + bd_Year, "%d %m %Y")
    timeNow = datetime.now()

    country = data.get('PacketData', 'country')

    if len(nuid) > 32 or len(nuid) < 3:  # Entered user name length is out of bounds
        toSend.set("PacketData", "errorContainer.[]", "1")
        toSend.set("PacketData", "errorCode", "21")
        toSend.set("PacketData", "localizedMessage", 'The required parameters for this call are missing or invalid')
        toSend.set("PacketData", "errorContainer.0.fieldName", "displayName")

        if len(nuid) > 32:
            toSend.set("PacketData", "errorContainer.0.fieldError", "3")
            toSend.set("PacketData", "errorContainer.0.value", "TOO_LONG")
            self.logger_err.new_message("[Register] Email " + nuid + " is too long!", 1)
        else:
            toSend.set("PacketData", "errorContainer.0.fieldError", "2")
            toSend.set("PacketData", "errorContainer.0.value", "TOO_SHORT")
            self.logger_err.new_message("[Register] Email " + nuid + " is too short!", 1)
    elif db.checkIfEmailTaken(nuid):  # Email is already taken
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "160")
        toSend.set("PacketData", "localizedMessage", 'That account name is already taken')
        self.logger_err.new_message("[Register] User with email " + nuid + " is already registered!", 1)
    elif timeNow.year - birthday.year - ((timeNow.month, timeNow.day) < (birthday.month, birthday.day)) < 18:  # New user is not old enough
        toSend.set("PacketData", "errorContainer.[]", "1")
        toSend.set("PacketData", "errorContainer.0.fieldName", "dob")
        toSend.set("PacketData", "errorContainer.0.fieldError", "15")
        toSend.set("PacketData", "errorCode", "21")
        self.logger_err.new_message("[Register] User with email " + nuid + " is too young to register new account!", 1)
    else:
        db.registerUser(nuid, password, str(birthday).split(" ")[0], country)
        self.logger.new_message("[Register] User " + nuid + " was registered successfully!", 1)

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuLogin(self, data):
    """ User is logging in with email and password """

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

    loginData = db.loginUser(nuid, password)

    if loginData['UserID'] > 0:  # Got UserID - Login Successful
        self.CONNOBJ.accountSessionKey = loginData['SessionID']
        self.CONNOBJ.userID = loginData['UserID']
        self.CONNOBJ.nuid = nuid

        toSend.set("PacketData", "lkey", loginData['SessionID'])
        toSend.set("PacketData", "nuid", nuid)

        if returnEncryptedInfo == 1:
            encryptedLoginData = "Ciyvab0tregdVsBtboIpeChe4G6uzC1v5_-SIxmvSL" + b64encode(nuid + "\f" + password)
            if encryptedLoginData.find('==') != -1:
                encryptedLoginData = encryptedLoginData.replace("==", '-_')
            else:
                encryptedLoginData = encryptedLoginData.replace("=", '-')

            toSend.set("PacketData", "encryptedLoginInfo", encryptedLoginData)

        toSend.set("PacketData", "profileId", str(loginData['UserID']))
        toSend.set("PacketData", "userId", str(loginData['UserID']))

        self.logger.new_message("[Login] User " + nuid + " logged in successfully!", 1)
    elif loginData['UserID'] == 0:  # The password the user specified is incorrect
        toSend.set("PacketData", "localizedMessage", "The password the user specified is incorrect")
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "122")

        self.logger_err.new_message("[Login] User " + nuid + " specified incorrect password!", 1)
    else:  # User not found
        toSend.set("PacketData", "localizedMessage", "The user was not found")
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "101")

        self.logger_err.new_message("[Login] User " + nuid + " does not exist", 1)

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuGetPersonas(self):
    """ Get personas associated with account """

    userID = self.CONNOBJ.userID
    personas = db.getUserPersonas(userID)

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuGetPersonas")
    toSend.set("PacketData", "personas.[]", str(len(personas)))

    personaId = 0
    for persona in personas:
        toSend.set("PacketData", "personas." + str(personaId), persona)
        personaId += 1

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuLoginPersona(self, data):
    """ User logs in with selected Persona """

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuLoginPersona")

    requestedPersonaName = data.get("PacketData", "name")

    personaData = db.loginPersona(self.CONNOBJ.userID, requestedPersonaName)
    if personaData is not None:
        self.CONNOBJ.personaID = personaData['personaId']
        self.CONNOBJ.personaSessionKey = personaData['lkey']
        self.CONNOBJ.personaName = requestedPersonaName

        toSend.set("PacketData", "lkey", personaData['lkey'])
        toSend.set("PacketData", "profileId", str(self.CONNOBJ.personaID))
        toSend.set("PacketData", "userId", str(self.CONNOBJ.personaID))

        self.logger.new_message("[Persona] User " + self.CONNOBJ.nuid + " just logged as " + requestedPersonaName, 1)
    else:
        toSend.set("PacketData", "localizedMessage", "The user was not found")
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "101")
        self.logger_err.new_message("[Persona] User " + self.CONNOBJ.nuid + " wanted to login as " + requestedPersonaName + " but this persona cannot be found!", 1)

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuAddPersona(self, data):
    """ User wants to add a Persona """

    name = data.get("PacketData", "name")

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuAddPersona")

    if len(name) > 16 or len(name) < 3:  # Entered persona name length is out of bounds
        toSend.set("PacketData", "errorContainer.[]", "1")
        toSend.set("PacketData", "errorCode", "21")
        toSend.set("PacketData", "localizedMessage", "The required parameters for this call are missing or invalid")
        toSend.set("PacketData", "errorContainer.0.fieldName", "displayName")

        if len(name) > 16:
            toSend.set("PacketData", "errorContainer.0.fieldError", "3")
            toSend.set("PacketData", "errorContainer.0.value", "TOO_LONG")

            self.logger_err.new_message("[Persona] User " + self.CONNOBJ.nuid + " wanted to create new persona, but name " + name + " is too long!", 1)
        else:
            toSend.set("PacketData", "errorContainer.0.fieldError", "2")
            toSend.set("PacketData", "errorContainer.0.value", "TOO_SHORT")

            self.logger_err.new_message("[Persona] User " + self.CONNOBJ.nuid + " wanted to create new persona, but name " + name + " is too short!", 1)
    elif db.checkIfPersonaNameExists(self.CONNOBJ.userID, name):
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "localizedMessage", "That account name is already taken")
        toSend.set("PacketData", "errorCode", "160")

        self.logger_err.new_message("[Persona] User " + self.CONNOBJ.nuid + " wanted to create new persona (" + name + "), but persona with this name is already registered in this account!", 1)
    else:
        db.addPersona(self.CONNOBJ.userID, name)

        self.logger.new_message("[Persona] User " + self.CONNOBJ.nuid + " just created new persona (" + name + ")", 1)

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuDisablePersona(self, data):
    """ User wants to remove a Persona """

    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuDisablePersona")

    personaToDisable = data.get("PacketData", "name")

    if db.checkIfPersonaNameExists(self.CONNOBJ.userID, personaToDisable):
        db.removePersona(self.CONNOBJ.userID, personaToDisable)

        self.logger.new_message("[Persona] User " + self.CONNOBJ.nuid + " just removed persona (" + personaToDisable + ")", 1)
    else:
        toSend.set("PacketData", "localizedMessage", "The data necessary for this transaction was not found")
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "104")
        self.logger_err.new_message("[Persona] User " + self.CONNOBJ.nuid + " wanted to remove persona (" + personaToDisable + "), but persona with this name didn't exist!", 1)

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleGetTelemetryToken(self):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "GetTelemetryToken")

    tokenbuffer = readFromConfig("connection", "emulator_ip")  # Messenger IP
    tokenbuffer += ","
    tokenbuffer += str(0)  # Messenger Port
    tokenbuffer += ","
    tokenbuffer += ",enUS,^Ů™¨Üś·Ć¤¤‰“ťĘ˙…Ź˛ŃĂÖ¬Ś±ďÄ±ˇ‚†Ś˛°ÄÝ±–†Ě›áî°ˇ‚†Ś°ŕŔ†Ě˛ąĘ‰»¦–Ĺ‚ťŠÔ©Ń©Ż„™’´ČŚ–±äŕł†Ś°îŔáŇĚŰŞÓ€"

    token = b64encode(tokenbuffer).replace("=", "%3d")

    toSend.set("PacketData", "telemetryToken", token)
    toSend.set("PacketData", "enabled", "CA,MX,PR,US,VI,AD,AF,AG,AI,AL,AM,AN,AO,AQ,AR,AS,AW,AX,AZ,BA,BB,BD,BF,BH,BI,BJ,BM,BN,BO,BR,BS,BT,BV,BW,BY,BZ,CC,CD,CF,CG,CI,CK,CL,CM,CN,CO,CR,CU,CV,CX,DJ,DM,DO,DZ,EC,EG,EH,ER,ET,FJ,FK,FM,FO,GA,GD,GE,GF,GG,GH,GI,GL,GM,GN,GP,GQ,GS,GT,GU,GW,GY,HM,HN,HT,ID,IL,IM,IN,IO,IQ,IR,IS,JE,JM,JO,KE,KG,KH,KI,KM,KN,KP,KR,KW,KY,KZ,LA,LB,LC,LI,LK,LR,LS,LY,MA,MC,MD,ME,MG,MH,ML,MM,MN,MO,MP,MQ,MR,MS,MU,MV,MW,MY,MZ,NA,NC,NE,NF,NG,NI,NP,NR,NU,OM,PA,PE,PF,PG,PH,PK,PM,PN,PS,PW,PY,QA,RE,RS,RW,SA,SB,SC,clntSock,SG,SH,SJ,SL,SM,SN,SO,SR,ST,SV,SY,SZ,TC,TD,TF,TG,TH,TJ,TK,TL,TM,TN,TO,TT,TV,TZ,UA,UG,UM,UY,UZ,VA,VC,VE,VG,VN,VU,WF,WS,YE,YT,ZM,ZW,ZZ")
    toSend.set("PacketData", "filters", "")
    toSend.set("PacketData", "disabled", "")

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuGetEntitlements(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuGetEntitlements")

    groupName = data.get("PacketData", "groupName")
    userID = self.CONNOBJ.userID

    userEntitlements = db.getUserEntitlements(userID)
    entitlements = []

    for entitlement in userEntitlements:
        if entitlement['groupName'] == groupName:
            entitlements.append(entitlement)

    count = 0
    for entitlement in entitlements:
        toSend.set("PacketData", "entitlements." + str(count) + ".grantDate", entitlement['grantDate'])
        toSend.set("PacketData", "entitlements." + str(count) + ".groupName", entitlement['groupName'])
        toSend.set("PacketData", "entitlements." + str(count) + ".userId", entitlement['userId'])
        toSend.set("PacketData", "entitlements." + str(count) + ".entitlementTag", entitlement['entitlementTag'])
        toSend.set("PacketData", "entitlements." + str(count) + ".version", entitlement['version'])
        toSend.set("PacketData", "entitlements." + str(count) + ".terminationDate", entitlement['terminationDate'])
        toSend.set("PacketData", "entitlements." + str(count) + ".productId", entitlement['productId'])
        toSend.set("PacketData", "entitlements." + str(count) + ".entitlementId", entitlement['entitlementId'])
        toSend.set("PacketData", "entitlements." + str(count) + ".status", entitlement['status'])
        toSend.set("PacketData", "entitlements." + str(count) + ".statusReasonCode", entitlement['statusReasonCode'])
        count += 1

    toSend.set("PacketData", "entitlements.[]", str(len(entitlements)))

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def HandleNuSearchOwners(self, data):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "NuSearchOwners")
    toSend.set("PacketData", "nameSpaceId", "battlefield")

    screenName = data.get("PacketData", "screenName").replace("_", "")
    searchResults = db.searchPersonas(screenName)

    if len(searchResults) != 0:
        count = 0
        for user in searchResults:
            if user['UserID'] != self.CONNOBJ.userID:  # Prevent self-adding
                toSend.set("PacketData", "users." + str(count) + ".id", str(user['PersonaID']))
                toSend.set("PacketData", "users." + str(count) + ".name", user['PersonaName'])
                toSend.set("PacketData", "users." + str(count) + ".type", "1")
                count += 1

        toSend.set("PacketData", "users.[]", str(count))
    else:
        toSend.set("PacketData", "errorContainer.[]", "0")
        toSend.set("PacketData", "errorCode", "104")
        toSend.set("PacketData", "localizedMessage", "The data necessary for this transaction was not found")

    Packet(toSend).send(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'GetCountryList':
        HandleGetCountryList(self)
    elif txn == 'NuGetTos':
        HandleNuGetTos(self)
    elif txn == 'NuAddAccount':
        HandleNuAddAccount(self, data)
    elif txn == 'NuLogin':
        HandleNuLogin(self, data)
    elif txn == 'NuGetPersonas':
        HandleNuGetPersonas(self)
    elif txn == 'NuLoginPersona':
        HandleNuLoginPersona(self, data)
    elif txn == 'NuAddPersona':
        HandleNuAddPersona(self, data)
    elif txn == 'NuDisablePersona':
        HandleNuDisablePersona(self, data)
    elif txn == 'GetTelemetryToken':
        HandleGetTelemetryToken(self)
    elif txn == 'NuGetEntitlements':
        HandleNuGetEntitlements(self, data)
    elif txn == 'NuSearchOwners':
        HandleNuSearchOwners(self, data)
    else:
        self.logger_err.new_message(
            "[" + self.ip + ":" + str(self.port) + ']<-- Got unknown acct message (' + txn + ")", 2)
