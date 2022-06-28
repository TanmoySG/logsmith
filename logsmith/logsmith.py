from logsmith.packages.constants import DefaultConfigurations, LogLevels
from logsmith.packages.logging import Driver
from logsmith.packages.monitor import Monitor
from logsmith.packages.utilities import File


class Logsmith:
    def __init__(self, configurations: dict) -> None:
        """
        Constructor to load configurations into the Logsmith Object.

        Args:
            configurations [dict] : dictionary with values for configurations.
        """
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

    def configure(self, configurations: dict) -> None:
        """
        configure() method helps to load configurations into the Logsmith Object.

        Args:
            configurations [dict] : dictionary with values for configurations.
        """
        self.env = configurations.get("env", self.env)
        self.logfile = configurations.get("logfile", self.logfile)
        self.console_only = configurations.get("console_only", self.console_only)
        self.logFormat = configurations.get("logFormat", self.logFormat)
        self.logStatementPattern = configurations.get(
            "logStatementPattern", self.logStatementPattern
        )
        self.monitorLogging = configurations.get("monitorLogging", self.monitorLogging)
        self.monitorConfigs = Monitor().getConfigs(configurations)
        pass

    def fetchConfigFromFile(self, filepath: str) -> None:
        """
        fetchConfigFromFile() method helps to load configurations from JSON Config Files.

        Args:
            filepath [str] : Path to the Configuration File
        """
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
        pass

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
        """
        INFO() is one of the logging methods that can be used for logging at Informational log level.

        Args:
            log [string | dict] : log to be published
        """
        Driver(loglevel=LogLevels.INFO, configs=self).run(log)

    def WARN(self, log):
        """
        WARN() is one of the logging methods that can be used for logging at Warning log level.

        Args:
            log [string | dict] : log to be published
        """
        Driver(loglevel=LogLevels.WARN, configs=self).run(log)

    def SUCCESS(self, log):
        """
        SUCCESS() is one of the logging methods that can be used for logging at Successful log level.

        Args:
            log [string | dict] : log to be published
        """
        Driver(loglevel=LogLevels.SUCCESS, configs=self).run(log)

    def FAILURE(self, log):
        """
        FAILURE() is one of the logging methods that can be used for logging at Failure log level.

        Args:
            log [string | dict] : log to be published
        """
        Driver(loglevel=LogLevels.FAILURE, configs=self).run(log)

    def CRITICAL(self, log):
        """
        CRITICAL() is one of the logging methods that can be used for logging at Critical log level.

        Args:
            log [string | dict] : log to be published
        """
        Driver(loglevel=LogLevels.CRITICAL, configs=self).run(log)

    def LOG(self, loglevel, log):
        """
        LOG() is one of the logging methods that can be used for logging with Custom log level.

        Args:
            loglevel [string]   : custom loglevel
            log [string | dict] : log to be published
        """
        Driver(loglevel=loglevel, configs=self).run(log)


class log(Logsmith):
    def __init__(self, configurations: dict) -> None:
        super().__init__(configurations)
