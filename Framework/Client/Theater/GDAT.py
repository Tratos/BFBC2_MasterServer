from Globals import Servers
from Utilities.Packet import Packet


def ReceiveRequest(self, data):
    try:
        lobbyID = str(data.get("PacketData", "LID"))
        gameID = str(data.get("PacketData", "GID"))
    except:
        lobbyID = None
        gameID = None

    if lobbyID is not None and gameID is not None:
        server = None

        for srv in Servers:
            if str(srv.serverData.get("ServerData", "LID")) == lobbyID and str(srv.serverData.get("ServerData", "GID")) == gameID:
                server = srv

        toSend = Packet().create()
        toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
        toSend.set("PacketData", "LID", lobbyID)
        toSend.set("PacketData", "GID", gameID)

        toSend.set("PacketData", "HU", str(server.personaID))
        toSend.set("PacketData", "HN", str(server.personaName))

        toSend.set("PacketData", "I", server.ipAddr)
        toSend.set("PacketData", "P", str(server.serverData.get("ServerData", "PORT")))  # Port

        toSend.set("PacketData", "N", str(server.serverData.get("ServerData", "NAME")))  # name of server in list
        toSend.set("PacketData", "AP", str(server.activePlayers))  # current number of players on server
        toSend.set("PacketData", "MP", str(server.serverData.get("ServerData", "MAX-PLAYERS")))  # Maximum players on server
        toSend.set("PacketData", "QP", str(server.serverData.get("ServerData", "B-U-QueueLength")))  # Something with the queue...lets just set this equal to B-U-QueueLength
        toSend.set("PacketData", "JP", str(server.joiningPlayers))  # Players that are joining the server right now?
        toSend.set("PacketData", "PL", "PC")  # Platform - PC / XENON / PS3

        # Constants
        toSend.set("PacketData", "PW", "0")  # ??? - its certainly not something like "hasPassword"
        toSend.set("PacketData", "TYPE", str(server.serverData.get("ServerData", "TYPE")))  # what type?? constant value - "G"
        toSend.set("PacketData", "J", str(server.serverData.get("ServerData", "JOIN")))  # ??? constant value - "O"

        # Userdata
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
        Packet(toSend).send(self, "GDAT", 0x00000000, 0)

        toSend = Packet().create()
        toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
        toSend.set("PacketData", "LID", lobbyID)
        toSend.set("PacketData", "GID", gameID)

        toSend.set("PacketData", "D-AutoBalance", server.serverData.get("ServerData", "D-AutoBalance"))
        toSend.set("PacketData", "D-Crosshair", server.serverData.get("ServerData", "D-Crosshair"))
        toSend.set("PacketData", "D-FriendlyFire", server.serverData.get("ServerData", "D-FriendlyFire"))
        toSend.set("PacketData", "D-KillCam", server.serverData.get("ServerData", "D-KillCam"))
        toSend.set("PacketData", "D-Minimap", server.serverData.get("ServerData", "D-Minimap"))
        toSend.set("PacketData", "D-MinimapSpotting", server.serverData.get("ServerData", "D-MinimapSpotting"))
        toSend.set("PacketData", "UGID", server.serverData.get("ServerData", "UGID"))
        toSend.set("PacketData", "D-ServerDescriptionCount", "0")  # Server Description? What is it? # TODO: Make support for Server Descriptions
        try:
            toSend.set("PacketData", "D-BannerUrl", server.serverData.get("ServerData", "D-BannerUrl"))
        except:
            pass
        toSend.set("PacketData", "D-ThirdPersonVehicleCameras", server.serverData.get("ServerData", "D-ThirdPersonVehicleCameras"))
        toSend.set("PacketData", "D-ThreeDSpotting", server.serverData.get("ServerData", "D-ThreeDSpotting"))

        playersData = []
        for i in range(32):
            if len(str(i)) == 1:
                curr = "0" + str(i)
            else:
                curr = str(i)

            pdat = server.serverData.get("ServerData", "D-pdat" + curr)

            if pdat != "|0|0|0|0":
                playersData.append(pdat)

        Packet(toSend).send(self, "GDET", 0x00000000, 0)

        for player in playersData:
            for playerOnServer in server.connectedPlayers:
                if playerOnServer.personaName == player.split('|')[0]:
                    toSend = Packet().create()
                    toSend.set("PacketData", "NAME", playerOnServer.personaName)
                    toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
                    toSend.set("PacketData", "PID", str(playerOnServer.playerID))
                    toSend.set("PacketData", "UID", str(playerOnServer.personaID))
                    toSend.set("PacketData", "LID", lobbyID)
                    toSend.set("PacketData", "GID", gameID)
                    Packet(toSend).send(self, "PDAT", 0x00000000, 0)
    else:
        toSend = Packet().create()
        toSend.set("PacketData", "TID", str(data.get("PacketData", "TID")))
        Packet(toSend).send(self, "GDAT", 0x00000000, 0)
