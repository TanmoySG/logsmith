from time import sleep
from logsmith import log

log = log()

log.configure(logfile="logs", console_only=False)

log.INFO("Information")
log.WARN("Warning")

log.configure(ENV="DEV", logfile="logs", console_only=True)

log.SUCCESS("Success!")
log.FAILURE("Failed")
log.CRITICAL("Critical")