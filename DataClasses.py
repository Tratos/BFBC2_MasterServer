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
    nuid = ""
    personaName = ""

    accountSessionKey = ""
    personaSessionKey = ""

    serverData = None

    plasmaPacketID = 0
    theaterPacketID = 0

    clientVersion = ""
    gameID = 0

    validServers = {'bfbc2.server.pc@ea.com': {'password': 'Che6rEPA', 'id': 1},  # Server NUIDL {'password': serverPassword, 'id': userID
                    'bfbc.server.ps3@ea.com': {'password': 'zAmeH7bR', 'id': 2},
                    'bfbc.server.xenon@ea.com': {'password': 'B8ApRavE', 'id': 3}}

    validPersonas = {"bfbc2.server.p": 1,  # PersonaName: PersonaID
                     "bfbc.server.ps": 2,
                     "bfbc.server.xe": 3}

    ipAddr = None
    networkInt = None
    theaterInt = None
    IsUp = False

    ping_timer = None
    memcheck_timer = None
