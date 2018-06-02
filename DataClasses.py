class Client:
    userID = 0
    personaID = 0
    nuid = ""
    personaName = ""

    accountSessionKey = ""
    personaSessionKey = ""

    plasmaPacketID = 0
    theaterPacketID = 0

    filteredServers = 0

    clientString = ""
    sku = ""
    locale = ""
    clientPlatform = ""
    clientVersion = ""
    SDKVersion = ""
    protocolVersion = ""
    fragmentSize = 0
    clientType = ""

    ipAddr = None
    networkInt = None
    theaterInt = None
    IsUp = False

    ping_timer = None
    memcheck_timer = None


class Server:
    userID = 0
    personaID = 0

    accountSessionKey = ""
    personaSessionKey = ""

    serverData = None

    plasmaPacketID = 0
    theaterPacketID = 0

    clientVersion = ""
    gameID = 0

    validPersonas = {"bfbc2.server.p": 1,
                     "bfbc.server.ps": 2,
                     "bfbc.server.xe": 3}

    ipAddr = None
    networkInt = None
    theaterInt = None
    IsUp = False

    ping_timer = None
    memcheck_timer = None
