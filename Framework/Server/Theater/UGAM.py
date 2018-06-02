def ReceivePacket(self, data):
    """ Update server info """

    for item in data.items("PacketData"):
        if item[0] != "TID":
            self.CONNOBJ.serverData.set("ServerData", item[0], str(item[1]).replace('"', ""))

    self.logger.new_message("[" + self.ip + ":" + str(self.port) + "] Updated server info!")
