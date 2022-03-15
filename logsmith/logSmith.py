from termcolor import colored
import datetime

LOG_MODE_COLORS = {
    "WARNING": "yellow",
    "INFO": "blue",
    "SUCCESS": "green",
    "FAILURE": "red",
    "CRITICAL": "grey"
}

def logToFile(filepath, logStatement)->None:
    with open(filepath, "a") as logfileObject:
        logfileObject.write(logStatement+"\n")


class log:

    def __init__(self) -> None:
        self.ENV="Default"
        self.logfile=None
        self.console_only=True
        pass

    def configure(self, console_only, ENV="default", logfile=None):
        self.ENV = ENV
        self.logfile = logfile
        self.console_only = console_only

        config_statement = ""

        if self.console_only != True:
            config_statement = f"[ {self.ENV} - Logging at {self.logfile} ]"
            logToFile(self.logfile, config_statement)
        else:
            config_statement= f"[ {self.ENV} - Logging to Console only ]"
        print(colored(text=config_statement, color="magenta",attrs=["bold"]))

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
        print(colored(text=log_statement, color=LOG_MODE_COLORS["CRITICAL"], on_color="on_red"))
