from dataclasses import dataclass
import os
from logsmith.packages.utilities import String

URITemplate = compile("{0}://{1}:{2}");

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
    def __init__(self, monitorConfig) -> None:
        if "monitor" in self.monitorConfig:
            return {}
        self.monitorConfig = monitorConfig
        pass

    def getConfigs(self) -> dict:
        if "monitor" in self.monitorConfig:
            return {}
        monitorConfigs = {}
        monitorConfigs.monitorPort = config.monitor.port || process.env.MONITOR_PORT
        monitorConfigs.monitorURI = config.monitor.server || process.env.MONITOR_URI
        monitorConfigs.monitorProtocol = config.monitor.protocol || process.env.MONITOR_PROTOCOL || "http"
        monitorConfigs.monitorListener = URITemplate(monitorConfigs.monitorProtocol, monitorConfigs.monitorURI, monitorConfigs.monitorPort) || process.env.LISTENER
        monitorConfigs.publisher = formatPublisherConfig(config.monitor.publisher)
        monitorConfigs.context = formatContextConfig(monitorConfigs.publisher.publisher, config.monitor.context)
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