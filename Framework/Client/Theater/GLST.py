from Globals import Servers
from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    """ Game List """

    toSend = Packet().create()
    toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
    toSend.set("PacketData", "LID", "1")
    toSend.set("PacketData", "LOBBY-NUM-GAMES", str(len(Servers)))
    toSend.set("PacketData", "LOBBY-MAX-GAMES", "1000")
    toSend.set("PacketData", "FAVORITE-GAMES", "0")
    toSend.set("PacketData", "FAVORITE-PLAYERS", "0")
    toSend.set("PacketData", "NUM-GAMES", str(len(Servers) - self.CONNOBJ.filteredServers))

    Packet(toSend).send(self, "GLST", 0x00000000, 0)

    if len(Servers) == 0 or self.CONNOBJ.filteredServers == len(Servers):
        self.CONNOBJ.filteredServers = 0
    else:
        """ Game Data """

        server = Servers[self.CONNOBJ.filteredServers]

        toSend = Packet().create()
        toSend.set("PacketData", "TID", str(self.CONNOBJ.theaterPacketID))
        toSend.set("PacketData", "LID", "1")  # id of lobby
        toSend.set("PacketData", "GID", str(server.serverData.get("ServerData", "GID")))  # id of game/server
        toSend.set("PacketData", "HN", server.personaName)  # account name of server (host name)
        toSend.set("PacketData", "HU", str(server.userID))  # account id of server (host user)
        toSend.set("PacketData", "N", str(server.serverData.get("ServerData", "NAME")))  # name of server in list

        if self.CONNOBJ.ipAddr[0] == server.ipAddr[0]:  # Client and Server has the same ip?
            toSend.set("PacketData", "I", server.serverData.get("ServerData", "INT-IP"))
            toSend.set("PacketData", "P", str(server.serverData.get("ServerData", "INT-PORT")))  # Port
        else:
            toSend.set("PacketData", "I", server.ipAddr[0])  # Client and Server are in diffirent networks, so send public ip of server
            toSend.set("PacketData", "P", str(server.serverData.get("ServerData", "PORT")))  # Port

        toSend.set("PacketData", "JP", str(server.joiningPlayers))  # Players that are joining the server right now?
        toSend.set("PacketData", "QP", str(server.serverData.get("ServerData", "B-U-QueueLength")))  # Something with the queue...lets just set this equal to B-U-QueueLength
        toSend.set("PacketData", "AP", str(server.activePlayers))  # current number of players on server
        toSend.set("PacketData", "MP", str(server.serverData.get("ServerData", "MAX-PLAYERS")))  # Maximum players on server
        toSend.set("PacketData", "PL", "PC")  # Platform - PC / XENON / PS3

        """ Constants """
        toSend.set("PacketData", "F", "0")  # ???
        toSend.set("PacketData", "NF", "0")  # ???
        toSend.set("PacketData", "J", str(server.serverData.get("ServerData", "JOIN")))  # ??? constant value - "O"
        toSend.set("PacketData", "TYPE", str(server.serverData.get("ServerData", "TYPE")))  # what type?? constant value - "G"
        toSend.set("PacketData", "PW", "0")  # ??? - its certainly not something like "hasPassword"

        """ Other server specific values """
        toSend.set("PacketData", "B-U-Softcore", str(server.serverData.get("ServerData", "B-U-Softcore")))  # Game is softcore - what does that mean?
        toSend.set("PacketData", "B-U-Hardcore", str(server.serverData.get("ServerData", "B-U-Hardcore")))  # Game is hardcore
        toSend.set("PacketData", "B-U-HasPassword", str(server.serverData.get("ServerData", "B-U-HasPassword")))  # Game has password
        toSend.set("PacketData", "B-U-Punkbuster", str(server.serverData.get("ServerData", "B-U-Punkbuster")))  # Game has punkbuster?
        toSend.set("PacketData", "B-U-EA", str(server.serverData.get("ServerData", "B-U-EA")))  # is server EA Orginal?
        toSend.set("PacketData", "B-version", str(server.serverData.get("ServerData", "B-version")))  # Version of the server (exact version) - TRY TO CONNECT TO ACTUAL VERSION OF SERVER
        toSend.set("PacketData", "V", str(server.clientVersion))  # "clientVersion" of server (shows up in server log on startup)
        toSend.set("PacketData", "B-U-level", str(server.serverData.get("ServerData", "B-U-level")))  # current map of server
        toSend.set("PacketData", "B-U-gamemode", str(server.serverData.get("ServerData", "B-U-gamemode")))  # Gameplay Mode (Conquest, Rush, SQDM,  etc)
        toSend.set("PacketData", "B-U-sguid", str(server.serverData.get("ServerData", "B-U-sguid")))  # Game PB Server GUID?
        toSend.set("PacketData", "B-U-Time", str(server.serverData.get("ServerData", "B-U-Time")))  # uptime of server?
        toSend.set("PacketData", "B-U-hash", str(server.serverData.get("ServerData", "B-U-hash")))  # Game hash?
        toSend.set("PacketData", "B-U-region", str(server.serverData.get("ServerData", "B-U-region")))  # Game region
        toSend.set("PacketData", "B-U-public", str(server.serverData.get("ServerData", "B-U-public")))  # Game is public
        toSend.set("PacketData", "B-U-elo", str(server.serverData.get("ServerData", "B-U-elo")))  # value that determines how good the players on the server are?

        toSend.set("PacketData", "B-numObservers", str(server.serverData.get("ServerData", "B-numObservers")))  # Observers = spectators? or admins?
        toSend.set("PacketData", "B-maxObservers", str(server.serverData.get("ServerData", "B-maxObservers")))  # Game max observers

        toSend.set("PacketData", "B-U-Provider", str(server.serverData.get("ServerData", "B-U-Provider")))  # provider id, figured out by server
        toSend.set("PacketData", "B-U-gameMod", str(server.serverData.get("ServerData", "B-U-gameMod")))  # maybe different value for vietnam here?
        toSend.set("PacketData", "B-U-QueueLength", str(server.serverData.get("ServerData", "B-U-QueueLength")))  # players in queue or maximum queue length? (sometimes smaller than QP (-1?))

        if server.serverData.get("ServerData", "B-U-Punkbuster") == 1:
            toSend.set("PacketData", "B-U-PunkBusterVersion", "1")

        Packet(toSend).send(self, "GDAT", 0x00000000, 0)
        self.CONNOBJ.filteredServers += 1
