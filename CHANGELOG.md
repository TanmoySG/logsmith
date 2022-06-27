# Changelogs

## Latest - v0.1.0

Whats new in this version?
- Support for Logsmith Monitor
- Configuration Changes
  - Added logformat, logStatementPattern, monitor parameters, among others
  - Monitor Configurations can be defined using the monitor parameter
- Added a custom Logging Method - `log.LOG(loglevel, log)` that supports logging at a user defined log level other than the ones available.
- Added `fetchConfigFromFile()` method to lod configurations from JSON Files
- `configure()` method required dictionary with configuration then of named parameters.
- Logs can be "transported" to monitor instances.
- Added Logsmith Class as main access point, and to maintain backward compatibility the log Class inherits from Logsmith and can be used interchangeably.

What's has changed?
- The top logging statement with the environment and where logs are published has been removed
- Colors for each method has been changed, only the loglevel are logged with colors on terminal 
- Phasing out environment (ENV)
- Even though the log class can be used interchangeably, it’ll be phased out in favour of "Logsmith"