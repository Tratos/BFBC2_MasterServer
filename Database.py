import sys
import sqlite3

from os.path import exists

from passlib.hash import pbkdf2_sha256

from Config import readFromConfig
from Logger import Log

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
                logger_err.new_message('There is an problem with initializing database!\nAdditional Error Info:\n' + str(DBError), 1)
                sys.exit(6)

    def initializeDatabase(self):
        tables = [{'Accounts': ['userID integer PRIMARY KEY AUTOINCREMENT UNIQUE', 'EMail string UNIQUE', 'Password string', 'Birthday string', 'Country string']}]

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
        password = pbkdf2_sha256.hash(password)

        try:
            cursor = self.connection.cursor()
            cursor.execute("INSERT INTO Accounts (EMail, Password, Birthday, Country) VALUES (?,?,?,?)", (email, password, birthday, country,))
            self.connection.commit()
            cursor.close()

            logger.new_message('Successfully registered new account (' + email + ')!', 1)
            return True
        except Exception, e:
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
