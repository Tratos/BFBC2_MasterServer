from Logger import Log

logger = Log("PlasmaClient", "\033[33;1m")
logger_err = Log("PlasmaClient", "\033[33;1;41m")


def HandleGoodbye(self, data):
    reason = data.get("PacketData", "reason")
    message = data.get("PacketData", "message")

    if reason == "GOODBYE_CLIENT_NORMAL":
        logger.new_message("[" + self.ip + ":" + str(self.port) + '][fsys] Client disconnected normally!', 2)
    else:
        logger_err.new_message("[" + self.ip + ":" + str(self.port) + "] Unknown Goodbye reason!", 2)
