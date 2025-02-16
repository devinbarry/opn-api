from typing import Any


class ParsingError(Exception):
    """
    Exception raised for errors in parsing data.

    Attributes:
        message (str): Explanation of the error.
        data (Any): The data that caused the error.
        details (str): Detailed information about the error.
    """

    def __init__(self, message: str, data: Any, details: str):
        self.message = message
        self.data = data
        self.details = details
        super().__init__(f"{message}: {details}")

    def __str__(self):
        return f"{self.message}: {self.details}"


class APIException(Exception):
    def __init__(self, *args, status_code=None, resp_body=None, url=None, **kwargs):
        self.resp_body = resp_body
        self.status_code = status_code
        self.url = url
        message = {
            "API client": kwargs.get("message", resp_body),
        }
        if url:
            message["url"] = url
        super(APIException, self).__init__(message, *args)
