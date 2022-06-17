import json


class StringTemplate:
    """
    StringTemplate Utility provides a cleaner interface for string templating with format
    """

    def __init__(self, template: str) -> None:
        """
        Constructor to pass the template string. 

        Args:
            template: string template with placeholders within {}
        """

        self.template = template
        return self

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
