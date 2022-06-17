from types import SimpleNamespace

DefaultLogStatementPattern = "[{timestamp}] {message}"

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
