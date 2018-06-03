import sqlite3
import sys

from os.path import exists
from time import strftime

from passlib.hash import pbkdf2_sha256

from Config import readFromConfig
from Logger import Log
from Utilities.RandomStringGenerator import GenerateRandomString

logger = Log("Database", "\033[37;1m")
logger_err = Log("Database", "\033[37;1;41m")


class Database(object):
    def __init__(self, showWelcomeMsg=False):
        dbFileLocation = readFromConfig("database", "db_file_path")

        if exists(dbFileLocation):
            if showWelcomeMsg:
                logger.new_message('Connected to database!', 1)
            self.connection = sqlite3.connect(dbFileLocation)
            self.cleanup()
        else:
            logger.new_message('Database file not found! Initializing database...', 1)
            self.connection = sqlite3.connect(dbFileLocation)
            try:
                self.initializeDatabase()
                logger.new_message('Database initialized successfully!', 1)
            except Exception as DBError:
                logger_err.new_message(
                    'There is an problem with initializing database!\nAdditional Error Info:\n' + str(DBError), 1)
                sys.exit(6)

    def initializeDatabase(self):
        tables = [{'Accounts': ['userID integer PRIMARY KEY AUTOINCREMENT UNIQUE', 'EMail string UNIQUE',
                                'Password string', 'Birthday string', 'Country string']},
                  {'Entitlements': ['userID integer', 'groupName string', 'entitlementId integer PRIMARY KEY AUTOINCREMENT UNIQUE', 'entitlementTag string', 'version integer', 'grantDate string', 'terminationDate string', 'productId string', 'status string', 'statusReasonCode string']},
                  {'Personas': ['personaID integer PRIMARY KEY AUTOINCREMENT UNIQUE', 'userID integer', 'personaName string']}]

        cursor = self.connection.cursor()

        for table in tables:
            sql = ""
            for name, columns in table.items():
                if len(sql) == 0:
                    sql = "CREATE TABLE " + name + " ("

                for column in columns:
                    sql += column + ','
                sql = sql[:-1]
                sql += ")"

            cursor.execute(sql)

        self.connection.commit()
        cursor.close()

    def cleanup(self):
        tables = []

        cursor = self.connection.cursor()

        for table in tables:
            cursor.execute("DELETE FROM " + table)

        self.connection.commit()
        cursor.close()

        cursor = self.connection.cursor()

        cursor.execute("VACUUM")

        self.connection.commit()

        cursor.close()

    def registerUser(self, email, password, birthday, country):
        hashed_password = pbkdf2_sha256.hash(password)

        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Accounts (EMail, Password, Birthday, Country) VALUES (?,?,?,?)",
                           (email, hashed_password, birthday, country,))
            self.connection.commit()
            cursor.close()

            self.addDefaultEntitlements(self.loginUser(email, password)['UserID'])

            logger.new_message('Successfully registered new account (' + email + ')!', 1)
            return True
        except:
            logger_err.new_message('User with this email (' + email + ') are currently registered!', 1)
            return False

    def checkIfEmailTaken(self, email):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Accounts WHERE EMail = ?", (email,))

        data = cursor.fetchone()

        if data is not None:
            return True
        else:
            return False

    def checkIfPersonaNameExists(self, userID, personaName):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Personas WHERE userID = ? AND personaName = ?", (userID, personaName,))

        data = cursor.fetchone()

        if data is not None:
            return True
        else:
            return False

    def registerSession(self):
        session = GenerateRandomString(27) + "."
        return session

    def loginUser(self, email, password):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Accounts WHERE EMail = ?", (email,))

        data = cursor.fetchone()

        if data is not None:
            if pbkdf2_sha256.verify(password, data[2]):
                session = self.registerSession()
                return {'UserID': data[0], 'SessionID': session}
            else:
                return {'UserID': 0}  # Provided password is incorrect
        else:
            return {'UserID': -1}  # User not found

    def getUserPersonas(self, userID):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Personas WHERE userID = ?", (userID,))

        data = cursor.fetchall()

        if data is None:
            return []

        personas = []
        for persona in data:
            personas.append(persona[2])

        return personas

    def loginPersona(self, userID, personaName):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Personas WHERE userID = ? AND personaName = ?", (userID, personaName,))

        data = cursor.fetchone()

        if data is None:
            return None
        else:
            personaId = data[0]
            session = self.registerSession()

            return {'lkey': session, 'personaId': personaId}

    def addPersona(self, userID, personaName):
        cursor = self.connection.cursor()
        cursor.execute("INSERT INTO Personas (userID, personaName) VALUES (?,?)", (userID, personaName,))

        self.connection.commit()
        cursor.close()

    def removePersona(self, userID, personaName):
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM Personas WHERE userID = ? AND personaName = ?", (userID, personaName,))

        self.connection.commit()
        cursor.close()

    def getUserEntitlements(self, userID):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Entitlements WHERE userID = ?", (userID,))

        data = cursor.fetchall()

        entitlements = []
        if data is not None:
            for entitlement in data:
                entitlements.append({'userId': str(entitlement[0]),
                                     'groupName': str(entitlement[1]),
                                     'entitlementId': str(entitlement[2]),
                                     'entitlementTag': str(entitlement[3]).replace(":", "%3a"),
                                     'version': str(entitlement[4]),
                                     'grantDate': str(entitlement[5]).replace(":", "%3a"),
                                     'terminationDate': str(entitlement[6]).replace(":", "%3a"),
                                     'productId': str(entitlement[7]).replace(":", "%3a"),
                                     'status': str(entitlement[8]),
                                     'statusReasonCode': str(entitlement[9])})
        return entitlements

    def addDefaultEntitlements(self, forUserID):
        currentTime = strftime('%Y-%m-%dT%H:%MZ')

        defaultEntitlements = [(forUserID, 'NoVetRank', "BFBC2NAM:PC:NOVETRANK", 0, currentTime, "", "", "ACTIVE", "",),
                               (forUserID, '', "ONLINE_ACCESS", 0, currentTime, "", "DR:156691300", "ACTIVE", "",),
                               (forUserID, 'AddsVetRank', "BFBC2:PC:ADDSVETRANK", 0, currentTime, "", "", "ACTIVE", "",),  # sometimes clients don't have this in the packet...whatever
                               (forUserID, 'BFBC2PC', 'BETA_ONLINE_ACCESS', 0, currentTime, "", "OFB-BFBC:19121", "ACTIVE", "",)]  # beta access is nice too (though it doesnt seem to affect anything)

        if readFromConfig("emulator", "new_players_have_vietnam"):
            defaultEntitlements.append((forUserID, 'BFBC2PC', "BFBC2:PC:VIETNAM_ACCESS", 0, currentTime, "", "DR:219316800", "ACTIVE", ""))
            defaultEntitlements.append((forUserID, 'BFBC2PC', "BFBC2:PC:VIETNAM_PDLC", 0, currentTime, "", "DR:219316800", "ACTIVE", ""))

        if readFromConfig("emulator", "new_players_have_premium"):
            defaultEntitlements.append((forUserID, 'BFBC2PC', "BFBC2:PC:LimitedEdition", 1, currentTime, "", "OFB-BFBC:19120", "ACTIVE", ""))

        if readFromConfig("emulator", "new_players_have_specact"):
            defaultEntitlements.append((forUserID, 'BFBC2PC', "BFBC2:PC:ALLKIT", 0, currentTime, "", "DR:192365600", "ACTIVE", ""))

        if readFromConfig("emulator", "new_players_are_veterans"):
            defaultEntitlements.append((forUserID, 'AddsVetRank', "BF3:PC:ADDSVETRANK", 0, currentTime, "", "OFB-EAST:40873", "ACTIVE", ""))

        for entitlement in defaultEntitlements:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Entitlements (userID, groupName, entitlementTag, version, grantDate, terminationDate, productId, status, statusReasonCode) VALUES (?,?,?,?,?,?,?,?,?)", entitlement)

            self.connection.commit()
            cursor.close()
