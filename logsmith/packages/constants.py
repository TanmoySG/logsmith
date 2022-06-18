from types import SimpleNamespace

DefaultLogStatementPattern = "[{timestamp}] {message}"



LogLevels = SimpleNamespace(
    **{
        "WARN": "WARN",
        "INFO": "INFO",
        "CRITICAL": "CRITICAL",
        "SUCCESS": "SUCCESS",
        "FAILURE": "FAILURE",
        "CUSTOM": "CUSTOM"
    }
)

LogFormats = SimpleNamespace(
    **{
        "JSON": "JSON",
        "Statement": "Statement"
    }
)

DefaultConfigurations = SimpleNamespace(
    **{
        "env": "default",
        "logfile": None,
        "console_only": True,
        "logFormat": LogFormats.JSON,
        "logStatementPattern": DefaultLogStatementPattern,
        "monitorLogging": False
    }
)
