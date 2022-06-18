from packages.constants import DefaultLogStatementPattern, DefaultConfigurations, LogFormats
from packages.utilities import String, File

from termcolor import colored
import datetime

LOG_MODE_COLORS = {
    "WARNING": "yellow",
    "INFO": "blue",
    "SUCCESS": "green",
    "FAILURE": "red",
    "CRITICAL": "grey"
}


def logToFile(filepath, logStatement) -> None:
    with open(filepath, "a") as logfileObject:
        logfileObject.write(logStatement+"\n")


class log:

    def __init__(self, configurations: dict) -> None:
        self.env = configurations.get("env" , DefaultConfigurations.env)
        self.logfile = configurations.get("logfile",  DefaultConfigurations.logfile)
        self.console_only = configurations.get("console_only", DefaultConfigurations.console_only)
        self.logFormat = configurations.get("logFormat", DefaultConfigurations.logFormat)
        self.logStatementPattern = configurations.get("logStatementPattern", DefaultConfigurations.logStatementPattern)
        self.monitorLogging = configurations.get("monitorLogging", DefaultConfigurations.monitorLogging)
        # self.monitorConfigs = getMonitorConfigs(configurations)
        self.compiledLogPattern = String.Template(self.logStatementPattern)
        pass

    def configure(self,  configurations: dict):
        self.env = configurations.get("env" , self.env)
        self.logfile = configurations.get("logfile",  self.logfile)
        self.console_only = configurations.get("console_only", self.console_only)
        self.logFormat = configurations.get("logFormat", self.logFormat)
        self.logStatementPattern = configurations.get("logStatementPattern", self.logStatementPattern)
        self.monitorLogging = configurations.get("monitorLogging", self.monitorLogging)
        # self.monitorConfigs = getMonitorConfigs(configurations)
        self.compiledLogPattern = String.Template(self.logStatementPattern)

    def fetchConfigFromFile(self, filepath : str):
        configurations = File.JSON.read(filepath)
        self.env = configurations.get("env" , DefaultConfigurations.env)
        self.logfile = configurations.get("logfile",  DefaultConfigurations.logfile)
        self.console_only = configurations.get("console_only", DefaultConfigurations.console_only)
        self.logFormat = configurations.get("logFormat", DefaultConfigurations.logFormat)
        self.logStatementPattern = configurations.get("logStatementPattern", DefaultConfigurations.logStatementPattern)
        self.monitorLogging = configurations.get("monitorLogging", DefaultConfigurations.monitorLogging)
        # self.monitorConfigs = getMonitorConfigs(configurations)
        self.compiledLogPattern = String.Template(self.logStatementPattern)
        

    def INFO(self, message):
        _timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_statement = f"({self.ENV}) [{_timestamp}] INFO : {message}"
        if self.console_only != True:
            logToFile(self.logfile, log_statement)
        print(colored(text=log_statement, color=LOG_MODE_COLORS["INFO"]))

    def WARN(self, message):
        _timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_statement = f"({self.ENV}) [{_timestamp}] WARNING : {message}"
        if self.console_only != True:
            logToFile(self.logfile, log_statement)
        print(colored(text=log_statement, color=LOG_MODE_COLORS["WARNING"]))

    def SUCCESS(self, message):
        _timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_statement = f"({self.ENV}) [{_timestamp}] SUCCESS : {message}"
        if self.console_only != True:
            logToFile(self.logfile, log_statement)
        print(colored(text=log_statement, color=LOG_MODE_COLORS["SUCCESS"]))

    def FAILURE(self, message):
        _timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_statement = f"({self.ENV}) [{_timestamp}] FAILURE : {message}"
        if self.console_only != True:
            logToFile(self.logfile, log_statement)
        print(colored(text=log_statement, color=LOG_MODE_COLORS["FAILURE"]))

    def CRITICAL(self, message):
        _timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_statement = f"({self.ENV}) [{_timestamp}] CRITICAL : {message}"
        if self.console_only != True:
            logToFile(self.logfile, log_statement)
        print(colored(text=log_statement,
              color=LOG_MODE_COLORS["CRITICAL"], on_color="on_red"))
