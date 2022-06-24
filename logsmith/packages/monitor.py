from dataclasses import dataclass
import os
from logsmith.packages.utilities import String

URITemplate =  String.Template("{0}://{1}:{2}");

class DefaultPublisherTemplate:
    Origin = String.Template("app.{0}.com")
    Description = String.Template("Logs Published by {0}")
    
class DefaultContextTemplate:
    Origin = String.Template("app.{0}.com/{1}")
    Description = String.Template("Log Published by {0} to context {1}")
    Kind = {
        "logs": []
    }


class Monitor:
    def __init__(self, monitorConfig=None) -> None:
        """

        """
        self.config = monitorConfig
        pass

    def getConfigs(self, config) -> dict:
        monitorConfigs = {}
        if "monitor" in config:
            return  monitorConfigs 
        monitorConfigs["monitorPort"] = config["monitor"].get("port" , os.environ["MONITOR_PORT"])
        monitorConfigs["monitorURI"] = config["monitor"].get("server" , os.environ["MONITOR_URI"])
        monitorConfigs["monitorProtocol"] = config["monitor"].get("protocol" , "http")
        monitorConfigs["monitorListener"] =  os.environ.get("LISTENER" , URITemplate.fill([monitorConfigs["monitorProtocol"], monitorConfigs["monitorURI"], monitorConfigs["monitorPort"]]))
        monitorConfigs["publisher"] = self.Publisher(config["monitor"]["publisher"]).getConfig()
        monitorConfigs["context"] = self.Context(publisher=monitorConfigs["publisher"]["publisher"], contextConfig=config["monitor"]["context"]).getConfig()
        return monitorConfigs

    class Publisher:
        def __init__(self, publisherConfig=None) -> None:
            self.configs = publisherConfig
            self.publisher = self.configs["publisher"]
            pass

        def getConfig(self):
            publisherConfig = {}
            publisherConfig["publisher"] = self.configs.get("publisher", os.environ["PUBLISHER"])
            publisherConfig["origin"] = self.configs.get("origin", DefaultPublisherTemplate.Origin.fill(data=[self.publisher]))
            publisherConfig["description"] = self.configs.get("description",  DefaultPublisherTemplate.Description.fill(data=[self.publisher]))
            return publisherConfig

    class Context():
        def __init__(self, publisher="default", contextConfig=None ) -> None:
            self.configs = contextConfig
            self.publisher = publisher
            self.context = self.configs["context"]
            pass

        def getConfig(self):
            contextConfig = {}
            contextConfig["context"] = self.configs.get("context", os.environ["CONTEXT"])
            contextConfig["origin"] = self.configs.get("origin", DefaultContextTemplate.Origin.fill(data=[self.publisher, self.context]))
            contextConfig["description"] = self.configs.get("description", DefaultPublisherTemplate.Description(data=[self.publisher, self.context]))
            contextConfig["kind"] = self.configs.get("kind", DefaultContextTemplate.Kind)
            return contextConfig