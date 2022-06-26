from logsmith.packages.constants import DefaultConfigurations, LogLevels
from logsmith.packages.logging import Driver
from logsmith.packages.monitor import Monitor
from logsmith.packages.utilities import File


def logToFile(filepath, logStatement) -> None:
    with open(filepath, "a") as logfileObject:
        logfileObject.write(logStatement + "\n")


class Logsmith:
    def __init__(self, configurations: dict) -> None:
        self.env = configurations.get("env", DefaultConfigurations.env)
        self.logfile = configurations.get("logfile", DefaultConfigurations.logfile)
        self.console_only = configurations.get(
            "console_only", DefaultConfigurations.console_only
        )
        self.logFormat = configurations.get(
            "logFormat", DefaultConfigurations.logFormat
        )
        self.logStatementPattern = configurations.get(
            "logStatementPattern", DefaultConfigurations.logStatementPattern
        )
        self.monitorLogging = configurations.get(
            "monitorLogging", DefaultConfigurations.monitorLogging
        )
        self.monitorConfigs = Monitor().getConfigs(configurations)
        pass

    def configure(self, configurations: dict):
        self.env = configurations.get("env", self.env)
        self.logfile = configurations.get("logfile", self.logfile)
        self.console_only = configurations.get("console_only", self.console_only)
        self.logFormat = configurations.get("logFormat", self.logFormat)
        self.logStatementPattern = configurations.get(
            "logStatementPattern", self.logStatementPattern
        )
        self.monitorLogging = configurations.get("monitorLogging", self.monitorLogging)
        self.monitorConfigs = Monitor().getConfigs(configurations)

    def fetchConfigFromFile(self, filepath: str):
        configurations = File.JSON().read(filepath)
        self.env = configurations.get("env", DefaultConfigurations.env)
        self.logfile = configurations.get("logfile", DefaultConfigurations.logfile)
        self.console_only = configurations.get(
            "consoleOnly", DefaultConfigurations.console_only
        )
        self.logFormat = configurations.get(
            "logFormat", DefaultConfigurations.logFormat
        )
        self.logStatementPattern = configurations.get(
            "logStatementPattern", DefaultConfigurations.logStatementPattern
        )
        self.monitorLogging = configurations.get(
            "monitorLogging", DefaultConfigurations.monitorLogging
        )
        self.monitorConfigs = Monitor().getConfigs(configurations)

    def prepareMonitor(self):
        """
        prepareMonitor() method initiates monitor connection, prepares the monitor 
        by creating the publisher and context, if they do not exist.

        Returns:
            status : status of prepare request
            scope  : the response of request returned
        """
        return Monitor(monitorConfig=self.monitorConfigs).prepare()

    def INFO(self, log):
        Driver(loglevel=LogLevels.INFO, configs=self).run(log)

    def WARN(self, log):
        Driver(loglevel=LogLevels.WARN, configs=self).run(log)

    def SUCCESS(self, log):
        Driver(loglevel=LogLevels.SUCCESS, configs=self).run(log)

    def FAILURE(self, log):
        Driver(loglevel=LogLevels.FAILURE, configs=self).run(log)

    def CRITICAL(self, log):
        Driver(loglevel=LogLevels.CRITICAL, configs=self).run(log)

    def LOG(self, loglevel, log):
        Driver(loglevel=loglevel, configs=self).run(log)


class log(Logsmith):
    def __init__(self, configurations: dict) -> None:
        super().__init__(configurations)
