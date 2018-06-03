from time import strftime
from threading import Timer

from Config import readFromConfig
from Utilities.Packet import Packet
from Utilities.RandomStringGenerator import GenerateRandomString


def HandleHello(self, data):
    toSend = Packet().create()

    self.CONNOBJ.clientVersion = data.get("PacketData", "clientVersion")
    currentTime = strftime('%b-%d-%Y %H:%M:%S UTC')

    toSend.set("PacketData", "domainPartition.domain", "eagames")
    toSend.set("PacketData", "messengerIp", readFromConfig("connection", "emulator_ip"))
    toSend.set("PacketData", "messengerPort", 0)  # Unknown data are being send to this port
    toSend.set("PacketData", "domainPartition.subDomain", "BFBC2")
    toSend.set("PacketData", "TXN", "Hello")
    toSend.set("PacketData", "activityTimeoutSecs", 0)  # We could let idle clients disconnect here automatically?
    toSend.set("PacketData", "curTime", currentTime)
    toSend.set("PacketData", "theaterIp", readFromConfig("connection", "emulator_ip"))
    toSend.set("PacketData", "theaterPort", readFromConfig("connection", "theater_server_port"))

    Packet(toSend).send(self, "fsys", 0x80000000, self.CONNOBJ.plasmaPacketID)

    self.CONNOBJ.IsUp = True

    SendMemCheck(self)


def SendMemCheck(self):
    toSend = Packet().create()

    toSend.set("PacketData", "TXN", "MemCheck")
    toSend.set("PacketData", "memcheck.[]", 0)
    toSend.set("PacketData", "type", 0)
    toSend.set("PacketData", "salt", GenerateRandomString(9))

    if self.CONNOBJ.IsUp:
        Packet(toSend).send(self, "fsys", 0x80000000, 0)


def HandleMemCheck(self):
    if self.CONNOBJ.memcheck_timer is None and self.CONNOBJ.ping_timer is None:  # Activate both ping and memcheck timers when we receive this
        self.CONNOBJ.memcheck_timer = Timer(500, SendMemCheck, [self, ])
        self.CONNOBJ.memcheck_timer.start()
        self.CONNOBJ.ping_timer = Timer(150, SendPing, [self, ])
        self.CONNOBJ.ping_timer.start()
    else:  # Restart timers
        self.CONNOBJ.memcheck_timer.cancel()
        self.CONNOBJ.ping_timer.cancel()

        self.CONNOBJ.memcheck_timer = Timer(500, SendMemCheck, [self, ])
        self.CONNOBJ.memcheck_timer.start()
        self.CONNOBJ.ping_timer = Timer(150, SendPing, [self, ])
        self.CONNOBJ.ping_timer.start()


def HandlePing(self):
    if self.CONNOBJ.ping_timer is None:
        self.CONNOBJ.ping_timer = Timer(150, SendPing, [self, ])
        self.CONNOBJ.ping_timer.start()
    else:
        self.CONNOBJ.ping_timer.cancel()

        self.CONNOBJ.ping_timer = Timer(150, SendPing, [self, ])
        self.CONNOBJ.ping_timer.start()


def SendPing(self):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "Ping")

    if self.CONNOBJ.IsUp:
        Packet(toSend).send(self, "fsys", 0x80000000, 0)


def HandleGoodbye(self, data):
    reason = data.get("PacketData", "reason")
    message = data.get("PacketData", "message")

    if reason == "GOODBYE_CLIENT_NORMAL":
        self.logger.new_message("[" + self.ip + ":" + str(self.port) + '][fsys] Server disconnected with this message: ' + message.replace("%3d", "="), 2)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + "] Unknown Goodbye reason!", 2)

    self.CONNOBJ.IsUp = False

    if self.CONNOBJ.memcheck_timer is None and self.CONNOBJ.ping_timer is None:
        self.CONNOBJ.memcheck_timer.cancel()
        self.CONNOBJ.ping_timer.cancel()


def HandleGetPingSites(self):
    toSend = Packet().create()
    toSend.set("PacketData", "TXN", "GetPingSites")

    emuIp = readFromConfig("connection", "emulator_ip")

    toSend.set("PacketData", "pingSite.[]", "4")
    toSend.set("PacketData", "pingSite.0.addr", emuIp)
    toSend.set("PacketData", "pingSite.0.type", "0")
    toSend.set("PacketData", "pingSite.0.name", "gva")
    toSend.set("PacketData", "pingSite.1.addr", emuIp)
    toSend.set("PacketData", "pingSite.1.type", "1")
    toSend.set("PacketData", "pingSite.1.name", "nrt")
    toSend.set("PacketData", "pingSite.2.addr", emuIp)
    toSend.set("PacketData", "pingSite.2.type", "2")
    toSend.set("PacketData", "pingSite.2.name", "iad")
    toSend.set("PacketData", "pingSite.3.addr", emuIp)
    toSend.set("PacketData", "pingSite.3.type", "3")
    toSend.set("PacketData", "pingSite.3.name", "sjc")
    toSend.set("PacketData", "minPingSitesToPing", "0")

    Packet(toSend).send(self, "fsys", 0x80000000, self.CONNOBJ.plasmaPacketID)


def ReceivePacket(self, data, txn):
    if txn == 'Hello':
        HandleHello(self, data)
    elif txn == 'MemCheck':
        HandleMemCheck(self)
    elif txn == 'Ping':
        HandlePing(self)
    elif txn == 'Goodbye':
        HandleGoodbye(self, data)
    elif txn == 'GetPingSites':
        HandleGetPingSites(self)
    else:
        self.logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown fsys message (' + txn + ")", 2)
