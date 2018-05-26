from Responses import *

from Logger import Log

logger_err = Log("PlasmaClient", "\033[33;1;41m")


def ReceivePacket(self, data, txn):
    if txn == 'Hello':
        Hello.Hello(self, data)
    else:
        logger_err.new_message("[" + self.ip + ":" + str(self.port) + ']<-- Got unknown fsys message (' + txn + ")", 2)
