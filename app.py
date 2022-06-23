from logsmith import Logsmith

log = Logsmith({})
log.fetchConfigFromFile(filepath="/workspaces/logsmith/configs/config.json")

log.INFO("Information")
log.WARN({"message": "Information"})
log.CRITICAL({"message": "Information"})
log.SUCCESS({"message": "Information"})
log.FAILURE({"message": "Information"})
log.LOG(loglevel="TRACING", log={"message": "Information"})
