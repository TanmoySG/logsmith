# # from time import sleep
# # from logsmith import log

# # log = log()

# # log.configure(logfile="logs", console_only=False)

# # log.INFO("Information")
# # log.WARN("Warning")

# # log.configure(ENV="DEV", logfile="logs", console_only=True)

# # log.SUCCESS("Success!")
# # log.FAILURE("Failed")
# # log.CRITICAL("Critical")

# sample = {
#     "name": "tanmoy",
#     "age": "22",
#     "gen": "F",
#     "pos" : "top"
# }

# # template_String = "My Name is {name} gender {gen}".format(**sample)

# # def template_filler(x):
# #     return "My Name is {name} gender {gen}".format(**x)

# # temp_helper = template_filler

# # print(temp_helper(sample))

# # sample_Arr = ("Tanmoy", "24")

# # tmplt_str = "My Name is {0}, age {1}".format(*sample_Arr)

# # print(tmplt_str)

# print(sample.get("pos", "bot"))


# from logsmith.packages.utilities import File, Terminal, String
# from logsmith.packages.logging import LOG, transform

# # sampfp = "/workspaces/logsmith/configs/config.json"

# # loglevel = String.Format(text="WARN").fit().enclose(
# #     start="[", end="]").finalize()

# # logLevel = Terminal.Format(loglevel).color(color="white")

# # log = Terminal.Format(File.JSON().read(sampfp)).toString()

# # logTBP = f"{logLevel} {log}"

# # Terminal.log(logTBP)

# # print(File.LOG().read("/workspaces/logsmith/configs/log.log"))

# File.LOG().write("/workspaces/logsmith/configs/log.log", data=("line1", "line2") )
# File.LOG().write("/workspaces/logsmith/configs/log.log", data={"key" : "val"})

from logsmith import Logsmith

log = Logsmith({})
log.fetchConfigFromFile(filepath="/workspaces/logsmith/configs/config.json")

log.INFO("Information")
log.INFO({"message": "Information"})
