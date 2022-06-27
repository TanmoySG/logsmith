# Logsmith

Logsmith is a Logging Library for python apps with support for [logsmith-monitor](https://github.com/TanmoySG/logsmith-monitor).

## Getting Started

Install Logsmith.py using [pip](https://pypi.org/project/logsmith)

```sh
pip install logsmith
```

Import the `Logsmith` object to use Logsmith.py 

```py
from logsmith import Logsmith

log = Logsmith({})

log.INFO("this is working fine")
```

To ensure backward compatibility, the previously usable class 'log', that was the main accss point to the library, inherits from the Logsmith class and can be used interchangeably with 'Logsmith' class. Example:

```
from logsmith import log

log = log({})

log.INFO("this is working fine")
```

But, the log class will be phased out in favour of the Logsmith class and hence we recommend using the Logsmith class in your code for future proofing.

#### Configurations

While a Logsmith.py supports a no-config setup, there are some configurations that can be tweaked as per need. [Read More](#configurations)

For Logsmith-Monitor Support, [go here.](#support-for-logsmith-monitor)

## Usage

Logsmith.py provides several Log Level based logging methods. It also provides a customizable logging method that can be used to log with a custom log level other than the ones provided. The methods can take both JSON and Statements as valid log.

### log.SUCCESS()

`log.SUCCESS()` can be used to log Successful events and actions. Example:

```py
log.SUCCESS({"test" : "passed"})
log.SUCCESS("The Tests Passed!")
```

### log.INFO()

`log.INFO()` can be used to log Informational messages/prompts. Example:

```py
log.INFO({"status" : "ok"})
log.INFO("The System is OK")
```

### log.WARN()

`log.WARN()` can be used to log Warnings. Example:

```py
log.WARN({"status" : "The system may be Vulnerable"})
log.WARN("The system may be Vulnerable")
```

### log.FAILURE()

`log.FAILURE()` can be used to log Failures. Example:

```py
log.FAILURE({"test" : "failed"})
log.FAILURE("The Tests Failed.")
```

### log.CRITICAL()

`log.CRITICAL()` can be used to log events that may lead to system shutdowns, data loss or other critically fatal events. Example:

```py
log.CRITICAL({"system" : "meltdown"})
log.CRITICAL("The system is Shutting Down.")
```

### log.LOG()

This method provides the custom log level logging capability. This method takes a parameter `loglevel` other than the log itself. The loglevel can be set to any string. Example:

```py
log.LOG(loglevel="TEST", {"test": "passed"})
log.LOG(loglevel="TEST", "The test Passed")
```

## Configurations

To use logsmith, certain configurations are required. If no configs are provided then the default values are set. A basic logsmith config looks something like this.

```json
{
    "env": "test",
    "logfile": "path/to/local/log/file",
    "consoleOnly": false,
    "logStatementPattern": "[ {component} ~ {logLevel} ] : {message}",
    "logFormat": "json",
    "monitorLogging": true
}
```

The Various flags/fields that can be configured are

| Field               | Description                                                                                                                                                                                 | Type    | Allowed Values                       | Default Value             |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- | ------------------------------------ | ------------------------- |
| env                 | Environment on which the app is running                                                                                                                                                     | string  | Any                                  | "default"                 |
| consoleOnly         | If consoleOnly is set to true then the logs will only be shown on the terminal, and wont be logged to any file                                                                              | boolean | `true` or `false`                    | true                      |
| logfile             | If logs are to be logged to a file, this field is used to specify the path to the logfile, works only if consoleOnly is false                                                               | string  | Relative Path to File                | null                      |
| logStatementPattern | The Pattern in which the log needs to be logged on console. [Read More.](#log-statement-patterns)                                                                                           | string  | Any String                           | `[{timestamp}] {message}` |
| logFormat           | The Format of Log                                                                                                                                                                           | string  | `json` or `statement`                | json                      |
| monitorLogging      | Flag that is set if logging to monitor is required. If set to true, logs will be published to monitor too. If set to true, monitor specific configurations are also required. [Read More]() | boolean | `true` or `false`                    | false                     |
| monitor             | A JSON field that is required to communicate with monitor. Works only is monitorLogging is set to true. Read the [Monitor Config Section](#monitor-configurations) for more                 | json    | [Read More](#monitor-configurations) | null                      |

### Using Configurations

Configurations can be defined and used in an application by creating the config json and passing it to the Logsmith object while initializing.

```py
from logsmith import Logsmith

logConfig = {
    "env": "test",
    "logfile": "path/to/local/log/file",
    "consoleOnly": False,
    "logStatementPattern": "[ {component} ~ {logLevel} ] : {message}",
    "logFormat": "json",
    "monitorLogging": True
}

log = Logsmith(logConfig)
```

Configurations may also be loaded from JSON files. Define the Configurations in a JSON file and load it using `fetchConfigFromFile()` method.

```py
from logsmith import Logsmith

log = Logsmith({})
log.fetchConfigFromFile(filepath="/path/to/config/file.json")
```

## Support for Logsmith Monitor

Logsmith Monitor (or simply Monitor) is a stand-alone logging Server for multi-component apps. Read about logsmith-monitor [here](https://github.com/TanmoySG/logsmith-monitor).

Logsmith.py supports logging to Monitor. It supports creation of Publishers and Context namespaces.

### Monitor Configurations

There are some specific connfigurations that are required to log to logsmith monitor. A basic and minimum configuration has the following fields, along with the configurations mentioned above. 

The Configurations for monitor support are defined as a JSON Object with "monitor" as the key.

```json
{
    "monitor": {
        "port": "8080",
        "server": "localhost",
        "publisher": {
            "publisher": "testapp001"
        },
        "context": {
            "context": "testcontext001"
        }
    }
}
```

The fields required for monitor support are

| Fields    | Description                                          | Type         | Allowed Values                |
| --------- | ---------------------------------------------------- | ------------ | ----------------------------- |
| server    | The address/URI where monitor is running             | URI (string) | URL                           |
| port      | The Port of the address where its running            | string       | Numeric and Valid PORT number |
| publisher | A JSON object to define the details of the Publisher | JSON Object  | JSON                          |
| context   | A JSON Object top specify the details of the Context | JSON Object  | JSON                          |

The `publisher` and `context` fields are used to define their respective configs. The bare minimum publisher and context information that must be provided are the namespaces. 

For Publisher Configurations, the field that needs to be put is the publisher name. Eg:
```json
"publisher": {
    "publisher": "<publsiher-name>"
}
```

For Context Configurations, the field that needs to be put is the context name. Eg:
```json
"context": {
    "context": "<context-name>"
}
```

There are other customizable fields for either. These fields are same as that defined for running Monitor. 

- [Read More about the configurations for Publisher](https://github.com/TanmoySG/logsmith-monitor/blob/main/documentation/README.md#register-a-publisher)
- [Read More about the configurations for Contexts](https://github.com/TanmoySG/logsmith-monitor/blob/main/documentation/README.md#register-a-context)

When these values are not mentioned/provided by the user, logsmith creates/generates those for you. So the Configuration Above becomes

```json
"monitorConfigs": {
    "monitorPort": "8080",
    "monitorURI": "localhost",
    "monitorProtocol": "http",
    "monitorListener": "http://localhost:8080",
    "publisher": {
        "publisher": "testapp001",
        "origin": "app.testapp001.com",
        "description": "Logs Published by testapp001"
    },
    "context": {
        "context": "testcontext001",
        "origin": "app.testapp001.com/testcontext001",
        "description": "Logs Published by testapp001",
        "kind": []
    }
}
```

### Initializing Monitor Connection

Logsmith provides a method - `prepareMonitor()`, to initialize a connection with the monitor. The method checks if the Publisher and Context Namespaces are available in monitor and creates them if not. 

```py
from logsmith import Logsmith

log = Logsmith({})
log.fetchConfigFromFile(filepath="/path/to/file.json")

// initialize Monitor
log.prepareMonitor()
```

## Know More

Some general information about some of the components in Logsmith.py.

### Log Statement Patterns

Log Statement Patterns are strings with placeholder that are used to print logs on-to the local console in the same format. The placeholders are identified by the names of the fields (in log) and placeholders names are defined in the string by enclosing them within curly-braces `{}`. 

Example Usage
```py
from logsmith import Logsmith

logStatementPattern = "{timestamp} > {status}"
log = Logsmith({"logStatementPattern" : logStatementPattern})

log.INFO({"timetamp": "11 AM", "status" : "ok", "action": "create"})
```

The above code logs a custom log statement
```
11 AM > ok
```

## Example Application

To test Logsmith and Logsmith-Monitor in Action, we created this example application. 

Startup Logsmith Monitor in Docker
```console
make run-monitor
make show-monitor
```

Start the example Python App (Script).
```console
python3 example.py
```

The logs should be printed both on the monitor as well as the example app terminal. Play around with the config for more customization.

## Known Issues

There are some issues that we are working on to solve. List of the known issues and their temporary remediation are available [here](./KNOWN_ISSUES.md).
