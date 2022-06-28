import time
from logsmith.packages.monitor import Monitor
from logsmith.packages.utilities import File, Terminal, String
from logsmith.packages.constants import LogFormats, LogLevels, ColorModes


def transform(data) -> dict:
    """
    transform() method converts any value into a JSON/dictionary 
    object by assigning it as a value to the key message.

    Args:
        data [any] : message/data to be converted

    Returns:
        dict object with the data as the value of the key message
    """
    return {"message": data}


def getColor(loglevel):
    """
    getColor() method returns the foreground and background colors based on the loglevel passed.

    Args:
        loglevel [str] : level of log
    
    Returns:
        color and bgcolor - foreground and background color values
    """
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
    """
    Driver class is an interface for running the log flow in a sequential manner
    """

    def __init__(self, loglevel, configs) -> None:
        """
        Constructor

        Args:
            loglevel [string] : Log Level for the log
            config [dict] : the logsmith configuration
        """
        self.monitorConfigs = configs.monitorConfigs
        self.console_only = configs.console_only
        self.logFormat = configs.logFormat
        self.logStatementPattern = configs.logStatementPattern
        self.logfile = configs.logfile
        self.monitorLogging = configs.monitorLogging
        self.loglevel = loglevel
        self.color, self.bgcolor = getColor(loglevel=loglevel)
        pass

    def run(self, log):
        """
        run() method runs the log flow and executes all steps in a deterministic and sequential fashion.

        Args:
            log [any] : log to be published
        """
        if type(log) != dict:
            log = transform(log)

        log["timestamp"] = int(time.time())
        log["loglevel"] = self.loglevel

        if self.console_only == False:
            File.LOG().write(filepath=self.logfile, data=log)

        logJSON = None

        if self.logFormat == LogFormats.Statement:
            logJSON = String.Template(self.logStatementPattern).fill(data=log)
        elif self.logFormat == LogFormats.JSON:
            logJSON = log

        if self.monitorLogging == True:
            Monitor(monitorConfig=self.monitorConfigs).log(log=log)

        loglevel = (
            String.Format(text=self.loglevel)
            .fit(width=8)
            .enclose(start="[", end="]")
            .finalize()
        )
        loglevel = Terminal.Format(text=loglevel).color(
            color=self.color, bgcolor=self.bgcolor
        )

        terminalFormattedLog = f"{loglevel} {logJSON}"

        Terminal.log(terminalFormattedLog)
