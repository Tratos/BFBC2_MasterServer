from Responses import *

from Logger import Log

logger = Log("PlasmaClient", "\033[33;1m")
logger_err = Log("PlasmaClient", "\033[33;1;41m")


def ReceivePacket(self, data, txn):
    if txn == 'Hello':
        logger.new_message("[" + self.ip + ":" + str(self.port) + '][fsys] Received Hello Packet!', 2)
        Hello.Hello(self, data)
    elif txn == 'MemCheck':
        logger.new_message("[" + self.ip + ":" + str(self.port) + '][fsys] Received MemCheck!', 2)
        MemCheck.ReceiveMemCheck(self)
    elif txn == 'Goodbye':
        logger.new_message("[" + self.ip + ":" + str(self.port) + '][fsys] Received Goodbye Packet!', 2)
        Goodbye.HandleGoodbye(self, data)
    else:
        logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown fsys message (' + txn + ")", 2)
