import time
from logsmith.packages.utilities import File, Terminal, String
from logsmith.packages.constants import LogFormats, LogLevels, ColorModes


def transform(log) -> dict:
    return {"message": log}


def getColor(loglevel):
    color, bgcolor = None, None
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
    else:
        color = ColorModes.CUSTOM
        bgcolor = None
    return color, bgcolor


class Driver:
    def __init__(self, loglevel, configs) -> None:
        self.console_only = configs.console_only
        self.logFormat = configs.logFormat
        self.logStatementPattern = configs.logStatementPattern
        self.logfile = configs.logfile
        self.loglevel = loglevel
        self.color, self.bgcolor = getColor(loglevel=loglevel)
        pass

    def run(self, log):
        if type(log) != dict:
            log = transform(log)

        log["timestamp"] = int(time.time())
        log["loglevel"] = self.loglevel

        if self.console_only == False:
            File.LOG().write(filepath=self.logfile, data=log)

        logbody = None

        if self.logFormat == LogFormats.Statement:
            logbody = String.Template(self.logStatementPattern).fill(data=log)
        elif self.logFormat == LogFormats.JSON:
            logbody = log

        loglevel = (
            String.Format(text=self.loglevel)
            .fit()
            .enclose(start="[", end="]")
            .finalize()
        )
        loglevel = Terminal.Format(text=loglevel).color(
            color=self.color, bgcolor=self.bgcolor
        )

        terminalFormattedLog = f"{loglevel} {logbody}"

        Terminal.log(terminalFormattedLog)
