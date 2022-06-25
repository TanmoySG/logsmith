import os

from logsmith.packages.utilities import Fetch, String
from logsmith.packages.constants import MonitorResponse


URITemplate = String.Template("{0}://{1}:{2}")


class Endpoints:
    API = String.Template("{0}/")
    Publisher = String.Template("{0}/publisher")
    CheckPublisher = String.Template("{0}/{1}")
    Context = String.Template("{0}/{1}/context")
    CheckContext = String.Template("{0}/{1}/{2}")
    Log = String.Template("{0}/{1}/{2}/logs")


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
        self.configurations = monitorConfig
        pass

    def check(self) -> dict:
        endpoint = Endpoints.API.fill(data=[self.configurations["monitorListener"]])
        status_code, response = Fetch(url=endpoint).GET()

        status = True
        if status_code != 200:
            status = False
        return status, response["scope"]

    def prepare(self):
        publisher = self.configurations["publisher"]
        context = self.configurations["context"]

        status, scope = self.Context(
            publisher=publisher["publisher"], configurations=self.configurations
        ).check()
        if scope == MonitorResponse.Publisher.missing:
            status, scope = self.Publisher(configurations=self.configurations).create()
            if scope == MonitorResponse.Publisher.success:
                status, scope = self.Context(
                    publisher=publisher["publisher"], configurations=self.configurations
                ).create()
                if scope == MonitorResponse.Context.success:
                    return True, scope
                else:
                    return False, scope
            else:
                return False, scope
        elif scope == MonitorResponse.Context.missing:
            status, scope = self.Context(
                publisher=publisher["publisher"], configurations=self.configurations
            ).create()
            if scope == MonitorResponse.Context.success:
                return True, scope
            else:
                return False, scope
        else:
            return False, scope

    def getConfigs(self, configurations) -> dict:
        monitorConfigs = {}
        if "monitor" not in configurations:
            return monitorConfigs
        monitorConfigs["monitorPort"] = configurations["monitor"]["port"]
        monitorConfigs["monitorURI"] = configurations["monitor"].get("server")
        monitorConfigs["monitorProtocol"] = configurations["monitor"].get(
            "protocol", "http"
        )
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
            configurations["monitor"]["publisher"]
        ).getConfig()
        monitorConfigs["context"] = self.Context(
            publisher=monitorConfigs["publisher"]["publisher"],
            configurations=configurations["monitor"]["context"],
        ).getConfig()
        return monitorConfigs

    def log(self, log):
        listener = self.configurations["monitorListener"]
        publisher = self.configurations["publisher"]["publisher"]
        context = self.configurations["context"]["context"]
        endpoint = Endpoints.Log.fill(data=[listener, publisher, context])
        payload = log
        status_code, response = Fetch(url=endpoint).POST(
            header=RequestHeaders.POST, payload=payload
        )

        status = True
        if status_code != 200:
            status = False

        return status, response["scope"]

    class Publisher:
        def __init__(self, configurations=None) -> None:
            self.configurations = configurations
            self.publisher = self.configurations["publisher"]
            pass

        def create(self):
            endpoint = Endpoints.Publisher.fill(
                data=[self.configurations["monitorListener"]]
            )
            payload = self.publisher
            status_code, response = Fetch(url=endpoint).POST(
                header=RequestHeaders.POST, payload=payload
            )

            status = True
            if status_code != 200:
                status = False

            return status, response["scope"]

        def check(self):
            endpoint = Endpoints.CheckPublisher.fill(
                data=[
                    self.configurations["monitorListener"],
                    self.publisher["publisher"],
                ]
            )
            status_code, response = Fetch(url=endpoint).GET(header=RequestHeaders.POST)

            status = True
            if status_code != 200:
                status = False

            return status, response["scope"]

        def getConfig(self):
            publisherConfig = {}
            publisherConfig["publisher"] = self.configurations["publisher"]
            publisherConfig["origin"] = self.configurations.get(
                "origin", DefaultPublisherTemplate.Origin.fill(data=[self.publisher])
            )
            publisherConfig["description"] = self.configurations.get(
                "description",
                DefaultPublisherTemplate.Description.fill(data=[self.publisher]),
            )
            return publisherConfig

    class Context:
        def __init__(self, publisher="default", configurations=None) -> None:
            self.configurations = configurations
            self.publisher = publisher
            self.context = self.configurations["context"]
            pass

        def create(self):
            endpoint = Endpoints.Context.fill(
                data=[self.configurations["monitorListener"], self.publisher]
            )
            payload = self.context
            status_code, response = Fetch(url=endpoint).POST(
                header=RequestHeaders.POST, payload=payload
            )

            status = True
            if status_code != 200:
                status = False

            return status, response["scope"]

        def check(self):
            endpoint = Endpoints.CheckContext.fill(
                data=[
                    self.configurations["monitorListener"],
                    self.publisher,
                    self.context["context"],
                ]
            )
            status_code, response = Fetch(url=endpoint).GET(header=RequestHeaders.POST)

            status = True
            if status_code != 200:
                status = False

            return status, response["scope"]

        def getConfig(self):
            contextConfig = {}
            contextConfig["context"] = self.configurations["context"]
            contextConfig["origin"] = self.configurations.get(
                "origin",
                DefaultContextTemplate.Origin.fill(data=[self.publisher, self.context]),
            )
            contextConfig["description"] = self.configurations.get(
                "description",
                DefaultPublisherTemplate.Description.fill(
                    data=[self.publisher, self.context]
                ),
            )
            contextConfig["kind"] = self.configurations.get(
                "kind", DefaultContextTemplate.Kind
            )
            return contextConfig
