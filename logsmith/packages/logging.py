import time
from packages.utilities import File, Terminal, String
from packages.constants import LogFormats


def transform(log) -> dict:
    return {"message": log}


class DRIVER:

    def __init__(self, logLevel, configs) -> None:
        self = configs
        self.loglevel = logLevel
        pass

    def run(self, log):
        if type(log) != dict:
            log = transform(log)

        log["timestamp"] = int(time.time())
        log["logLevel"] = self.logLevel

        if self.console_only == False:
            File.LOG().write(filepath=self.logfile, data=log)

        terminalFormattedLog = None
        if self.logFormat == LogFormats.Statement:
            terminalFormattedLog = String.Template(self.logStatementPattern).fill(data=log)
        elif self.logFormat == LogFormats.JSON:
            terminalFormattedLog = log

        
