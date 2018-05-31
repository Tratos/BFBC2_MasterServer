class Client:
    userID = 0
    personaName = ""
    nuid = ""

    plasmaPacketID = 0

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
