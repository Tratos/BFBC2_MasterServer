from os.path import exists

from ConfigParser import ConfigParser

from Logger import Log
from Utilities.Packet import Packet

logger = Log("PlasmaClient", "\033[33;1m")
logger_err = Log("PlasmaClient", "\033[33;1;41m")


def HandleGetCountryList(self):
    countryList = GetCountryList(self)

    Packet(countryList).sendPacket(self, "acct", 0xb0000000, self.CONNOBJ.plasmaPacketID)
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


def ReceivePacket(self, data, txn):
    if txn == 'GetCountryList':  # User wants to create a new account
        HandleGetCountryList(self)
        logger.new_message("[" + self.ip + ":" + str(self.port) + '][acct] Received GetCountryList Request!', 2)
    else:
        logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown acct message (' + txn + ")", 2)
