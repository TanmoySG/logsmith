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
    """
    Monitor class provides the access point to every monitor-related actions. 
    """
    def __init__(self, monitorConfig=None) -> None:
        """ 
        Constructor to initialize monitor object with monitor configuration

        Args:
            monitorConfig [dict] : dict object with monitor configurations. 
            Pass the json value with the key - monitor
        """
        self.configurations = monitorConfig
        pass

    def check(self):
        """
        check() method checks if the monitor API is live or not.

        Returns:
            response of the API if live
        """
        endpoint = Endpoints.API.fill(data=[self.configurations["monitorListener"]])
        status_code, response = Fetch(url=endpoint).GET()

        status = True
        if status_code != 200:
            status = False
        return status, response["scope"]

    def prepare(self):
        """
        prepare() method initiates monitor connection, prepares the monitor
        by creating the publisher and context, if they do not exist.

        Returns:
            status [bool] : if the action was successful or not
            scope  [dict] : the response of request
        """
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
        """
        getConfigs() method prepares the complete monitor configuration from the minimal configurations.

        Args:
            configurations [dict] : configurations loaded into the Logsmith method

        Returns:
            complete configuration of monitor

        Refer: https://github.com/TanmoySG/logsmith-monitor/tree/main/libraries/js/logsmith#monitor-configurations
        """
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
        """
        log() method helps in connecting to monitor and publishes logs to the monitor.

        Args:
            log [any] : log to be pubished to monitor.

        Returns:
            status [bool] : True if request was successful, else False
            response [string] : Scope of response
        """
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
        """
        Monitor.Publisher class provides a common interface for all monitor-publisher functions
        """
        def __init__(self, configurations=None) -> None:
            """
            Constructor of Publisher

            Args:
                configurations [dict] : monitor configurations dict
            """
            self.configurations = configurations
            self.publisher = self.configurations["publisher"]
            pass

        def create(self):
            """
            create() method creates the publisher from the configurations

            Returns:
                status [bool]   : True if successfull, else False
                scope  [string] : Scope of response
            """
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
            """
            check() method checks if the publisher namespace exists in monitor

            Returns:
                status [bool]   : True if successfull, else False
                scope  [string] : Scope of response
            """
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
            """
            getConfig() method creates the publisher configurations

            Returns:
                publisher configs
            """
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
        """
        Monitor.Context class provides a common interface for all monitor-context functions
        """
        def __init__(self, publisher=None, configurations=None) -> None:
            """
            Constructor of Context

            Args:
                publisher [string] : name of the publisher namespace 
                configurations [dict] : monitor configurations dict
            """
            self.configurations = configurations
            self.publisher = publisher
            self.context = self.configurations["context"]
            pass

        def create(self):
            """
            create() method creates the context from the configurations

            Returns:
                status [bool]   : True if successfull, else False
                scope  [string] : Scope of response
            """
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
            """
            check() method checks if the context namespace exists in monitor

            Returns:
                status [bool]   : True if successfull, else False
                scope  [string] : Scope of response
            """
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
            """
            getConfig() method creates the context configurations

            Returns:
                context configurations
            """
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
