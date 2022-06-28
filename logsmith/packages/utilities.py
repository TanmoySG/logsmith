import json
import requests
from termcolor import colored


class String:
    """
    String provides a common interface for custom string methods
    """

    class Format:
        """
        String.Format provides a common interface for string formatting
        """

        def __init__(self, text: str) -> None:
            """
            Constructor to pass formatable string

            Args:
                text [str] : text to be formatted
            """

            self.text = text

        def __str__(self) -> str:
            """
            When the object of String.Format class is passed through str() method the value of text is returned
            """
            return self.text

        def fit(self, width: int = 8):
            """
            fit() allows the string to be fit into a given width

            Args:
                width [int] : the width to fit the string into. Default width is 8

            Returns:
                The string of desired length
            """

            self.text = self.text.ljust(width)[:width]
            return self

        def enclose(self, within=None, start=None, end=None):
            """
            enclose() allows the string to be enclosed by characters

            Args:
                within [str] : the characters that encloses the string on both ends
                start  [str] : the character to enclose the start of the string. start = within, when using within.
                end    [str] : the character to enclose the end of the string. end = within, when using within.
            """

            if within != None:
                start = within
                end = within

            self.text = f"{start}{self.text}{end}"
            return self

        def finalize(self) -> str:
            """
            finalize() can be called once all the string operations are complete. It returns the string.

            Returns:
                the formatted string value
            """
            return self.text

    class Template:
        """
        String.Template Utility provides a cleaner interface for string templating with format
        """

        def __init__(self, template: str) -> None:
            """
            Constructor to pass the template string.

            Args:
                template: string template with placeholders within {}
            """

            self.template = template
            pass

        def fill(self, data):
            """
            Method to fill the data in placeholders of the template

            Args:
                data [ dict | list | tuple ] : data to be mapped on the template based on the key or index

            Returns:
                Formatted string with values in placeholders
            """

            if type(data) == dict:
                return self.template.format(**data)
            elif type(data) in [list, tuple]:
                return self.template.format(*data)


class File:
    """
    File utility provides a common gateway to all file based operations.
    """

    class LOG:
        """
        File.LOG provides a common interface for all LOG file operations
        """

        def isLOG(self, filepath: str) -> bool:
            """
            isLOG() provides utility to check if given file is .log or not

            Args:
                filepath [str] :  path to the file

            Returns:
                Boolean value of true or false
            """

            if filepath.lower().endswith(".log"):
                return True
            return False

        def read(self, filepath: str) -> list:
            """
            read() provides the interface to read a .log file

            Args:
                filepath [str] : path to file

            Returns:
                A list with lines from the file
            """

            if not self.isLOG(filepath=filepath):
                raise ValueError(f"Only .log file supported, got {filepath}")

            with open(filepath) as log_file:
                data = [line.rstrip() for line in log_file]
            return data

        def write(self, filepath: str, data: any):
            """
            write() provides the interface to write to a .log file (in append mode). It creates the file if it doesn't exists.

            Args:
                filepath [str] : path to file
                data     [any] : data to be written
            """

            if not self.isLOG(filepath=filepath):
                raise ValueError(f"Only .log file supported, got {filepath}")

            lines = data if type(data) in [list, tuple] else [data]
            with open(file=filepath, mode="a+") as logfile:
                for line in lines:
                    logfile.write(f"{line}\n")

    class JSON:
        """
        File.JSON provides a common interface for all JSON file operations.
        """

        def isJSON(self, filepath: str) -> bool:
            """
            isJSON() provides utility to check if given file is json or not

            Args:
                filepath [str] :  path to the JSON file

            Returns:
                Boolean value of true or false
            """
            if filepath.lower().endswith(".json"):
                return True
            return False

        def read(self, filepath: str) -> dict:
            """
            read() provides the utility to read JSON files

            Args:
                filepath [str] : path to the JSON file

            Returns:
                parsed JSON data in a Dictionary interface

            Raises:
                ValueError if File is not of type JSON
            """

            if not self.isJSON(filepath=filepath):
                raise ValueError(f"Only .json file supported, got {filepath}")
            data = {}
            with open(filepath) as json_file:
                data = json.load(json_file)
            return data


class Terminal:
    """
    Terminal Utility provides a Common Interface for all Terminal related
    """

    def log(log) -> None:
        """
        log() method prints the log with the defined colors and bgcolor

        Args:
            level [str] : level of the log. Level is printed in color.
            log   [any] : data to be logged on the terminal. Can be of any type, converted to string pre-printing
        """

        log = str(log)
        print(log)

    class Format:
        def __init__(self, text: str) -> None:
            """
            Constructor to Initiate with text to be formatted for terminal

            Args:
                text [str] : text to be formatted
            """

            self.text = text
            pass

        def color(self, color="white", bgcolor=None) -> str:
            """
            color() method to format with color

            Args:
                color   [str] : color of string
                bgcolor [str] : color of background of string

            Returns:
                Colored and Formatted String that can be printed on terminal
            """

            color = color
            bgcolor = f"on_{bgcolor}" if bgcolor != None else None
            return colored(text=self.text, color=color, on_color=bgcolor)

        def toString(self) -> str:
            """
            toString() method returns the value of the loggable string when called on the object

            Returns:
                value of text
            """
            return str(self.text)


class Fetch:
    """
    Fetch utility provides a wrapper interface on requests module to perform requests.
    """

    def __init__(self, url: str) -> None:
        """
        Constructor to define URL.

        Args:
            url [str] : URL of Endpoint to be fetched
        """
        self.url = url
        pass

    def POST(self, header=None, payload=None):
        """
        POST() method provides a wrapper over request.post()

        Args:
            header [dict] : dictionary of headers for the request.
            payload [any] : payload/data to be posted.
        """
        response = requests.post(url=self.url, headers=header, json=payload)
        return response.status_code, response.json()

    def GET(self, header=None):
        """
        GET() method provides a wrapper over request.get()

        Args:
            header [dict] : dictionary of headers for the request.
        """
        response = requests.get(url=self.url, headers=header)
        return response.status_code, response.json()
