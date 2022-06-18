import json
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

        def fit(self, width: int = 8) -> str:
            """
            fit() allows the string to be fit into a given width

            Args:
                width [int] : the width to fit the string into. Default width is 8

            Returns:
                The string of desired length
            """

            return self.text.ljust(width)[:width]

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

    class JSON:
        """
        File.JSON provides a common interface for all JSON file operations.
        """

        def read(filepath: str) -> dict:
            """
            read() provides the utility to read JSON files 

            Args:
                filepath [str] : path to the JSON file

            Returns:
                parsed JSON data in a Dictionary interface

            Raises:
                ValueError if File is not of type JSON
            """

            if not filepath.lower().endswith(".json"):
                raise ValueError(f"Only JSON file supported, got {filepath}")
            data = {}
            with open(filepath) as json_file:
                data = json.load(json_file)
            return data


class Terminal:
    """
    Terminal Utility provides a Common Interface for all Terminal related 
    """

    def __init__(self, color="white", bgcolor=None) -> None:
        """
        Constructor

        Args:
            color [str] : color of string
            bgcolor [str] : color of background of string
        """

        self.color = color
        self.bgcolor = f"on_{bgcolor}" if bgcolor != None else None
        pass

    def log(self, level, log) -> None:
        """
        log() method prints the log with the defined colors and bgcolor

        Args:
            level [str] : level of the log. Level is printed in color.
            log [any] : data to be logged on the terminal. Can be of any type, converted to string pre-printing
        """

        log = str(log)
        level = f"[{level}]"
        print(colored(text=level, color=self.color, on_color=self.bgcolor), log)
