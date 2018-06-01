from ConfigParser import ConfigParser
from base64 import b64encode
from struct import pack, unpack

from Logger import Log


class Packet(object):
    def __init__(self, packet_data):
        self.packet_data = packet_data

    def generateChecksum(self, packet_id, PacketCount):
        PacketID = self.generatePacketID(packet_id + PacketCount)
        PacketLength = self.generatePacketLength()

        return PacketID + PacketLength

    def generatePacketID(self, packet_id):
        return pack(">I", packet_id)

    def generatePacketLength(self):
        return pack(">I", len(self.packet_data) + 12)

    def getPacketID(self, packet_id):
        return unpack(">I", packet_id)[0]

    def verifyPacketLength(self, packet_length):
        data_len = pack(">I", len(self.packet_data))

        if data_len == packet_length:
            return True
        else:
            return False

    def dataInterpreter(self):
        data = self.packet_data.split("\n")
        data.remove('\x00')  # Remove NULL from data

        dataObj = ConfigParser()
        dataObj.optionxform = str

        dataObj.add_section("PacketData")  # Will save all packet data to PacketData section

        for entry in data:
            parameter = entry.split("=", 1)[0]
            value = entry.split("=", 1)[1]

            dataObj.set("PacketData", parameter, value)

        return dataObj

    def generatePackets(self, packet_type, packet_id, PacketCount):
        packetData = self.packet_data.items("PacketData")

        self.packet_data = ""

        for entry in packetData:
            parameter = entry[0]
            value = entry[1]

            try:
                if value.find(" ") != -1:
                    self.packet_data += parameter + "=" + '"' + str(value) + '"' + "\n"
                else:
                    self.packet_data += parameter + "=" + str(value) + "\n"
            except AttributeError:
                self.packet_data += parameter + "=" + str(value) + "\n"

        self.packet_data = self.packet_data[:-1]

        if len(self.packet_data) > 8096:  # packet exceeds max size, base64 encode it and send it in chunks (can only happen in ssl connection?)
            decoded_size = len(self.packet_data)
            self.packet_data = b64encode(self.packet_data)
            encoded_size = len(self.packet_data)

            packet_data = [self.packet_data[i:i + 8096] for i in range(0, len(self.packet_data), 8096)]

            packets = []

            for data in packet_data:
                packetData = "decodedSize=" + str(decoded_size) + "\n"
                packetData += "size=" + str(encoded_size) + "\n"
                packetData += "data=" + str(data.replace("=", "%3d")) + "\x00"

                self.packet_data = packetData

                newPacket = packet_type
                newPacket += self.generateChecksum(0xb0000000, PacketCount)
                newPacket += self.packet_data

                packets.append(newPacket)

            return packets
        else:
            self.packet_data += "\x00"

            newPacket = packet_type
            newPacket += self.generateChecksum(packet_id, PacketCount)
            newPacket += self.packet_data

            return [newPacket]

    def sendPacket(self, network, packet_type, packet_id, PacketCount, udpAddr=None, logger=None):
        packets = self.generatePackets(packet_type, packet_id, PacketCount)

        if packets > 1:  # More than 1 packet
            for packet in packets:
                if udpAddr is None:
                    network.transport.write(packet)
                    logger.new_message("[" + network.ip + ":" + str(network.port) + ']--> ' + repr(packet), 3)
                else:
                    network.transport.write(packet, udpAddr)
                    logger.new_message("[" + udpAddr[0] + ":" + str(udpAddr[1]) + ']--> ' + repr(packet), 3)

        else:
            if udpAddr is None:
                network.transport.write(packets[0])
                logger.new_message("[" + network.ip + ":" + str(network.port) + ']--> ' + repr(packets[0]), 3)
            else:
                network.transport.write(packets[0], udpAddr)
                logger.new_message("[" + udpAddr[0] + ":" + str(udpAddr[1]) + ']--> ' + repr(packets[0]), 3)
