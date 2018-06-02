class Client:
    userID = 0
    personaID = 0
    nuid = ""
    personaName = ""

    accountSessionKey = ""
    personaSessionKey = ""

    plasmaPacketID = 0
    theaterPacketID = 0

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

    ipAddr = None
    networkInt = None
    IsUp = False

    ping_timer = None
    memcheck_timer = None
