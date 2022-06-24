import os

import requests
from logsmith.packages.utilities import String


class Endpoints:
    API = String.Template("{0}/")
    Publisher = String.Template("{0}/publisher")
    checkPublisher = String.Template("{0}/{1}")
    Context = String.Template("{0}/{1}/context")
    checkContext = String.Template("{0}/{1}/{2}")
    Log = String.Template("{0}/{1}/{2}/logs")


URITemplate = String.Template("{0}://{1}:{2}")


class DefaultPublisherTemplate:
    Origin = String.Template("app.{0}.com")
    Description = String.Template("Logs Published by {0}")


class DefaultContextTemplate:
    Origin = String.Template("app.{0}.com/{1}")
    Description = String.Template("Log Published by {0} to context {1}")
    Kind = {"logs": []}


class RequestHeaders:
    POST = {"Content-Type": "application/json"}


class Monitor:
    def __init__(self, monitorConfig=None) -> None:
        """ """
        self.config = monitorConfig
        pass

    def check(self) -> dict:
        endpoint = Endpoints.API.fill(data=[self.config["monitorListener"]])
        r = requests.get(url=endpoint)
        return r.json()

    def initiate(self):
        pass

    def getConfigs(self, config) -> dict:
        monitorConfigs = {}
        if "monitor" not in config:
            return monitorConfigs
        monitorConfigs["monitorPort"] = config["monitor"]["port"]
        monitorConfigs["monitorURI"] = config["monitor"].get("server")
        monitorConfigs["monitorProtocol"] = config["monitor"].get("protocol", "http")
        monitorConfigs["monitorListener"] = os.environ.get(
            "LISTENER",
            URITemplate.fill(
                [
                    monitorConfigs["monitorProtocol"],
                    monitorConfigs["monitorURI"],
                    monitorConfigs["monitorPort"],
                ]
            ),
        )
        monitorConfigs["publisher"] = self.Publisher(
            config["monitor"]["publisher"]
        ).getConfig()
        monitorConfigs["context"] = self.Context(
            publisher=monitorConfigs["publisher"]["publisher"],
            contextConfig=config["monitor"]["context"],
        ).getConfig()
        return monitorConfigs

    def log(self):
        pass

    class Publisher:
        def __init__(self, publisherConfig=None) -> None:
            self.configs = publisherConfig
            self.publisher = self.configs["publisher"]
            pass

        def create(self):
            pass

        def check(self):
            pass

        def getConfig(self):
            publisherConfig = {}
            publisherConfig["publisher"] = self.configs["publisher"]
            publisherConfig["origin"] = self.configs.get(
                "origin", DefaultPublisherTemplate.Origin.fill(data=[self.publisher])
            )
            publisherConfig["description"] = self.configs.get(
                "description",
                DefaultPublisherTemplate.Description.fill(data=[self.publisher]),
            )
            return publisherConfig

    class Context:
        def __init__(self, publisher="default", contextConfig=None) -> None:
            self.configs = contextConfig
            self.publisher = publisher
            self.context = self.configs["context"]
            pass

        def create(self):
            pass

        def check(self):
            pass

        def getConfig(self):
            contextConfig = {}
            contextConfig["context"] = self.configs["context"]
            contextConfig["origin"] = self.configs.get(
                "origin",
                DefaultContextTemplate.Origin.fill(data=[self.publisher, self.context]),
            )
            contextConfig["description"] = self.configs.get(
                "description",
                DefaultPublisherTemplate.Description.fill(
                    data=[self.publisher, self.context]
                ),
            )
            contextConfig["kind"] = self.configs.get(
                "kind", DefaultContextTemplate.Kind
            )
            return contextConfig
