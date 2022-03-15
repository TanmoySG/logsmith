from time import sleep
from logsmith import log

log = log()
log.configure(ENV="DEV", logfile="logs", console_only=True)


log.INFO("Information")
sleep(2)
log.WARN("Warning")
sleep(2)
log.SUCCESS("Success!")
sleep(2)
log.FAILURE("Failed")

log.CRITICAL("Critical")