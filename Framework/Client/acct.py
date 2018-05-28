# -*- coding: utf-8 -*-

from os.path import exists

from ConfigParser import ConfigParser

from Logger import Log
from Utilities.Packet import Packet

from urllib import quote

logger = Log("PlasmaClient", "\033[33;1m")
logger_err = Log("PlasmaClient", "\033[33;1;41m")


def HandleGetCountryList(self):
    countryList = GetCountryList(self)

    Packet(countryList).sendPacket(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)
    self.CONNOBJ.plasmaPacketID += 1


def GetCountryList(self):
    countryList = ConfigParser()
    countryList.optionxform = str
    countryList.add_section("PacketData")

    if exists("Data/countryLists/countryList_" + self.CONNOBJ.locale):
        with open("Data/countryLists/countryList_" + self.CONNOBJ.locale) as countryListFile:
            countryListData = countryListFile.readlines()
    else:
        with open("Data/countryLists/default") as countryListFile:
            countryListData = countryListFile.readlines()

    countryList.set("PacketData", "TXN", "GetCountryList")
    countryList.set("PacketData", "countryList.[]", str(len(countryListData)))

    countryId = 0
    for line in countryListData:
        countryList.set("PacketData", "countryList." + str(countryId) + ".ISOCode", line.split("=")[0])
        countryList.set("PacketData", "countryList." + str(countryId) + ".description",
                        line.split("=")[1].replace('"', "").replace("\n", ""))
        countryId += 1

    return countryList


def HandleNuGetTos(self, data):
    tos = GetTOS(self)

    Packet(tos).sendPacket(self, "acct", 0x80000000, self.CONNOBJ.plasmaPacketID)
    self.CONNOBJ.plasmaPacketID += 1


def GetTOS(self):
    tos = ConfigParser()
    tos.optionxform = str
    tos.add_section("PacketData")
    tos.set("PacketData", "TXN", "NuGetTos")
    tos.set("PacketData", "version", "20426_17.20426_17")
    print(self.CONNOBJ.locale)
    if exists("Data/termsOfUse/termsOfUse_" + self.CONNOBJ.locale):
        with open("Data/termsOfUse/termsOfUse_" + self.CONNOBJ.locale) as termsOfUseFile:
            termsOfUse = termsOfUseFile.read()
    else:
        with open("Data/termsOfUse/default") as termsOfUseFile:
            termsOfUse = termsOfUseFile.read()

    termsOfUse = quote(termsOfUse, safe=" ,.'&/()?;®@§[]").replace("%3A", "%3a").replace("%0A", "%0a") + "%0a%0a%09Battlefield%3a Bad Company 2 Master Server Emulator by B1naryKill3r%0ahttps://github.com/B1naryKill3r/BFBC2_MasterServer"
    tos.set("PacketData", "tos", termsOfUse)
    return tos


def ReceivePacket(self, data, txn):
    if txn == 'GetCountryList':  # User wants to create a new account
        HandleGetCountryList(self)
        logger.new_message("[" + self.ip + ":" + str(self.port) + '][acct] Received GetCountryList Request!', 2)
    elif txn == 'NuGetTos':
        HandleNuGetTos(self, data)
        logger.new_message("[" + self.ip + ":" + str(self.port) + '][acct] Received NuGetTos Request!', 2)
    else:
        logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown acct message (' + txn + ")", 2)
