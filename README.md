# logsmith
A Logging Library for Python

## Install

```
pip install logsmith
```

## Usage 

```
from logsmith import log

log = log()

log.INFO("Information")
log.WARN("Warning")
log.SUCCESS("Success!")
log.FAILURE("Failed")
log.CRITICAL("Critical")
```

### Run with Configurations

logsmith supports three flags - 

`ENV` [String] Enviroment used for Logging. Takes the name of Environment as String.

`console_only` [Boolean] Takes value `true` or `false`. Logs only to console if set to `true`.

`logfile` [String] Takes path of loggingfile as string. 

```
from logsmith import log

log = log()

log.configure(ENV="DEV", logfile="logs", console_only=True)

log.INFO("Information")
```

## 