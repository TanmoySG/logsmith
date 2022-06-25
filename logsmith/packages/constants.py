from types import SimpleNamespace

DefaultLogStatementPattern = "[{timestamp}] {message}"

ColorModes = SimpleNamespace(
    **{
        "WARN": "yellow",
        "INFO": "blue",
        "SUCCESS": "green",
        "FAILURE": "red",
        "CRITICAL": "grey",
        "CUSTOM": "white",
    }
)

LogLevels = SimpleNamespace(
    **{
        "WARN": "WARN",
        "INFO": "INFO",
        "CRITICAL": "CRITICAL",
        "SUCCESS": "SUCCESS",
        "FAILURE": "FAILURE",
        "CUSTOM": "CUSTOM",
    }
)

LogFormats = SimpleNamespace(**{"JSON": "json", "Statement": "statement"})

DefaultConfigurations = SimpleNamespace(
    **{
        "env": "default",
        "logfile": None,
        "console_only": True,
        "logFormat": LogFormats.JSON,
        "logStatementPattern": DefaultLogStatementPattern,
        "monitorLogging": False,
    }
)

class MonitorResponse:
    class Publisher:
        exists = "publisher.exists"
        invalid = "publisher.invalid"
        success = "publisher.success"
        missing = "publisher.missing"

    class Context:
        exists = "context.exists"
        invalid = "context.invalid"
        success = "context.success"
        missing = "context.missing"

    class Log:
        error = "log.error"
        success = "log.success"

    class Connection:
        failed = "connection.failed"
        success = "connection.success"