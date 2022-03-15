from termcolor import colored
import datetime

LOG_MODE_COLORS = {
    "WARNING": "yellow",
    "INFO": "blue",
    "SUCCESS": "green",
    "FAILURE": "red",
    "CRITICAL": "grey"
}


class log:

    def __init__(self) -> None:
        self.ENV="default"
        self.logfile=None
        self.console_only=True
        pass

    def configure(self, ENV, logfile, console_only):
        self.ENV = ENV
        self.logfile = logfile
        self.console_only = console_only

        config_statement = ""

        if self.console_only != True:
            config_statement = f"[ {self.ENV} - Logging at {self.logfile} ]"
            
        else:
            config_statement= f"[ {self.ENV} - Logging to Console only ]"
        print(colored(text=config_statement, color="magenta",attrs=["bold"]))

    def INFO(self, message):
        _timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_statement = f"[{_timestamp}] INFO : {message}"
        print(colored(text=log_statement, color=LOG_MODE_COLORS["INFO"]))

    def WARN(self, message):
        _timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_statement = f"[{_timestamp}] WARNING : {message}"
        print(colored(text=log_statement, color=LOG_MODE_COLORS["WARNING"]))

    def SUCCESS(self, message):
        _timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_statement = f"[{_timestamp}] SUCCESS : {message}"
        print(colored(text=log_statement, color=LOG_MODE_COLORS["SUCCESS"]))

    def FAILURE(self, message):
        _timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_statement = f"[{_timestamp}] FAILURE : {message}"
        print(colored(text=log_statement, color=LOG_MODE_COLORS["FAILURE"]))

    def CRITICAL(self, message):
        _timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log_statement = f"[{_timestamp}] CRITICAL : {message}"
        print(colored(text=log_statement, color=LOG_MODE_COLORS["CRITICAL"], on_color="on_red"))
