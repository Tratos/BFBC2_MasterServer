from ConfigParser import ConfigParser

from Globals import Servers
from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    """ Game List """
    newPacket = ConfigParser()
    newPacket.optionxform = str
    newPacket.add_section("PacketData")
    newPacket.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
    newPacket.set("PacketData", "LID", "1")
    newPacket.set("PacketData", "LOBBY-NUM-GAMES", str(len(Servers)))
    newPacket.set("PacketData", "LOBBY-MAX-GAMES", "1000")
    newPacket.set("PacketData", "FAVORITE-GAMES", "0")
    newPacket.set("PacketData", "FAVORITE-PLAYERS", "0")
    newPacket.set("PacketData", "NUM-GAMES", str(len(Servers)))

    Packet(newPacket).sendPacket(self, "GLST", 0x00000000, 0)

    if len(Servers) == 0:
        pass
    else:
        """ Game Data """
        print(Servers)
        for server in Servers:
            newPacket = ConfigParser()
            newPacket.optionxform = str
            newPacket.add_section("PacketData")
            newPacket.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
            newPacket.set("PacketData", "LID", "1")  # id of lobby
            newPacket.set("PacketData", "GID", str(server.serverData.get("ServerData", "GID")))  # id of game/server
            newPacket.set("PacketData", "HN", server.personaName)  # account name of server (host name)
            newPacket.set("PacketData", "HU", str(server.userID))  # account id of server (host user)
            newPacket.set("PacketData", "N", str(server.serverData.get("ServerData", "NAME")))  # name of server in list

            if self.CONNOBJ.ipAddr[0] == server.ipAddr[0]:  # Client and Server has the same ip?
                newPacket.set("PacketData", "I", server.serverData.get("ServerData", "INT-IP"))
                newPacket.set("PacketData", "P", str(server.serverData.get("ServerData", "INT-PORT")))  # Port
            else:
                newPacket.set("PacketData", "I", server.ipAddr[0])  # Client and Server are in diffirent networks, so send public ip of server
                newPacket.set("PacketData", "P", str(server.serverData.get("ServerData", "PORT")))  # Port

            newPacket.set("PacketData", "JP", "0")  # Players that are joining the server right now?
            newPacket.set("PacketData", "QP", str(server.serverData.get("ServerData",
                                                                        "B-U-QueueLength")))  # Something with the queue...lets just set this equal to B-U-QueueLength
            newPacket.set("PacketData", "AP", "0")  # current number of players on server
            newPacket.set("PacketData", "MP",
                          str(server.serverData.get("ServerData", "MAX-PLAYERS")))  # Maximum players on server
            newPacket.set("PacketData", "PL", "PC")  # Platform - PC / XENON / PS3

            """ Constants """
            newPacket.set("PacketData", "F", "0")  # ???
            newPacket.set("PacketData", "NF", "0")  # ???
            newPacket.set("PacketData", "J",
                          str(server.serverData.get("ServerData", "JOIN")))  # ??? constant value - "O"
            newPacket.set("PacketData", "TYPE",
                          str(server.serverData.get("ServerData", "TYPE")))  # what type?? constant value - "G"
            newPacket.set("PacketData", "PW", "0")  # ??? - its certainly not something like "hasPassword"

            """ Other server specific values """
            newPacket.set("PacketData", "B-U-Softcore",
                          str(server.serverData.get("ServerData",
                                                    "B-U-Softcore")))  # Game is softcore - what does that mean?
            newPacket.set("PacketData", "B-U-Hardcore",
                          str(server.serverData.get("ServerData", "B-U-Hardcore")))  # Game is hardcore
            newPacket.set("PacketData", "B-U-HasPassword",
                          str(server.serverData.get("ServerData", "B-U-HasPassword")))  # Game has password
            newPacket.set("PacketData", "B-U-Punkbuster",
                          str(server.serverData.get("ServerData", "B-U-Punkbuster")))  # Game has punkbuster?
            newPacket.set("PacketData", "B-U-EA",
                          str(server.serverData.get("ServerData", "B-U-EA")))  # is server EA Orginal?

            newPacket.set("PacketData", "B-version", str(server.serverData.get("ServerData",
                                                                               "B-version")))  # Version of the server (exact version) - TRY TO CONNECT TO ACTUAL VERSION OF SERVER
            newPacket.set("PacketData", "V",
                          str(server.clientVersion))  # "clientVersion" of server (shows up in server log on startup)
            newPacket.set("PacketData", "B-U-level",
                          str(server.serverData.get("ServerData", "B-U-level")))  # current map of server
            newPacket.set("PacketData", "B-U-gamemode", str(
                server.serverData.get("ServerData", "B-U-gamemode")))  # Gameplay Mode (Conquest, Rush, SQDM,  etc)
            newPacket.set("PacketData", "B-U-sguid",
                          str(server.serverData.get("ServerData", "B-U-sguid")))  # Game PB Server GUID?
            newPacket.set("PacketData", "B-U-Time",
                          str(server.serverData.get("ServerData", "B-U-Time")))  # uptime of server?
            newPacket.set("PacketData", "B-U-hash", str(server.serverData.get("ServerData", "B-U-hash")))  # Game hash?
            newPacket.set("PacketData", "B-U-region",
                          str(server.serverData.get("ServerData", "B-U-region")))  # Game region
            newPacket.set("PacketData", "B-U-public",
                          str(server.serverData.get("ServerData", "B-U-public")))  # Game is public
            newPacket.set("PacketData", "B-U-elo", str(server.serverData.get("ServerData",
                                                                             "B-U-elo")))  # value that determines how good the players on the server are?

            newPacket.set("PacketData", "B-numObservers", str(
                server.serverData.get("ServerData", "B-numObservers")))  # Observers = spectators? or admins?
            newPacket.set("PacketData", "B-maxObservers",
                          str(server.serverData.get("ServerData", "B-maxObservers")))  # Game max observers

            newPacket.set("PacketData", "B-U-Provider", str(
                server.serverData.get("ServerData", "B-U-Provider")))  # provider id, figured out by server
            newPacket.set("PacketData", "B-U-gameMod", str(
                server.serverData.get("ServerData", "B-U-gameMod")))  # maybe different value for vietnam here?
            newPacket.set("PacketData", "B-U-QueueLength", str(server.serverData.get("ServerData",
                                                                                     "B-U-QueueLength")))  # players in queue or maximum queue length? (sometimes smaller than QP (-1?))

            if server.serverData.get("ServerData", "B-U-Punkbuster") == 1:
                newPacket.set("PacketData", "B-U-PunkBusterVersion", "1")

            Packet(newPacket).sendPacket(self, "GDAT", 0x00000000, 0)
