import time
from packages.utilities import File, Terminal, String
from packages.constants import LogFormats, LogLevels, ColorModes


def transform(log) -> dict:
    return {"message": log}


def getColor(loglevel):
    color, bgcolor = None
    if loglevel == LogLevels.WARN:
        color = ColorModes.WARN
        bgcolor = None
    elif loglevel == LogLevels.INFO:
        color = ColorModes.INFO
        bgcolor = None
    elif loglevel == LogLevels.SUCCESS:
        color = ColorModes.SUCCESS
        bgcolor = None
    elif loglevel == LogLevels.FAILURE:
        color = ColorModes.FAILURE
        bgcolor = None
    elif loglevel == LogLevels.CRITICAL:
        color = ColorModes.CRITICAL
        bgcolor = "red"
    elif loglevel == LogLevels.CUSTOM:
        color = ColorModes.CUSTOM
        bgcolor = None
    return color, bgcolor


class Driver:

    def __init__(self, logLevel, configs) -> None:
        self = configs
        self.loglevel = logLevel
        self.color , self.bgcolor = getColor(loglevel=logLevel)
        pass

    def run(self, log):
        if type(log) != dict:
            log = transform(log)

        log["timestamp"] = int(time.time())
        log["logLevel"] = self.logLevel

        if self.console_only == False:
            File.LOG().write(filepath=self.logfile, data=log)

        logbody= None
        if self.logFormat == LogFormats.Statement:
            logbody = String.Template(self.logStatementPattern).fill(data=log)
        elif self.logFormat == LogFormats.JSON:
            logbody = log

        loglevel = String.Format(text=self.loglevel).fit().enclose(start="[", end="]").finalize()
        loglevel = Terminal.Format(text=loglevel).color(color=self.color, bgcolor=self.bgcolor)

        terminalFormattedLog = f"{loglevel} {logbody}"

        Terminal.log(terminalFormattedLog)
