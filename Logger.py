from Config import readFromConfig
from time import gmtime, strftime


from colorama import init


class Log(object):
    def __init__(self, messageFrom, messageColor):
        init()

        self.messageFrom = messageFrom
        self.messageColor = messageColor

        self.logFile = readFromConfig("debug", "create_log")
        self.logTimestamp = readFromConfig("debug", "put_timestamp_in_log")
        self.fileLogLevel = int(readFromConfig("debug", "file_log_level"))
        self.consoleLogLevel = int(readFromConfig("debug", "console_log_level"))

        self.useColors = readFromConfig("console", "use_colors")

    def new_message(self, message, level=0):
        timestamp = str(strftime("%H:%M:%S", gmtime()))

        if self.logFile:
            if level <= self.fileLogLevel:
                saveToLog = ""
                if self.logTimestamp:
                    saveToLog += "[" + timestamp + "]"

                saveToLog += "[" + self.messageFrom + "]"

                saveToLog += " " + message + "\n"

                with open("server.log", "a") as logfile:
                    logfile.write(saveToLog)

        if level <= self.consoleLogLevel:
            consoleMessage = "[" + timestamp + "]" + "[" + self.messageFrom + "] " + message

            if self.useColors:
                consoleMessage = self.messageColor + consoleMessage + "\33[0m"

            print(consoleMessage)
