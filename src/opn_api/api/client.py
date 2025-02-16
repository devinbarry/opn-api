import requests
from urllib3.exceptions import InsecureRequestWarning
from opn_api.exceptions import APIException
import json
from dataclasses import dataclass

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

HTTP_SUCCESS = (200, 201, 202, 203, 204, 205, 206, 207)


@dataclass
class OPNsenseClientConfig:
    """
    Configuration for OPNsense API client.

    Attributes:
        api_key (str): API key for authentication.
        api_secret (str): API secret for authentication.
        base_url (str): Base URL of the OPNsense API.
        ssl_verify_cert (bool): Whether to verify SSL certificates. Defaults to True.
        ca (Optional[str]): Path to CA certificate file. Defaults to None.
        timeout (int): Timeout for API requests in seconds. Defaults to 60.
    """

    api_key: str
    api_secret: str
    base_url: str
    ssl_verify_cert: bool = True
    ca: str | None = None
    timeout: int = 60


class OPNAPIClient:
    def __init__(self, config: OPNsenseClientConfig):
        self._config = config

    @property
    def ssl_verify_cert(self):
        if self._config.ssl_verify_cert:
            return self._config.ca
        return self._config.ssl_verify_cert

    def _process_response(self, response):
        if response.status_code in HTTP_SUCCESS:
            return self._parse_response(response)
        else:
            raise APIException(response=response.status_code, resp_body=response.text, url=response.url)

    @staticmethod
    def _parse_response(response):
        content_type = response.headers.get("content-type").split(";")[0]
        if content_type == "application/json":
            return json.loads(response.text)

        return response.text

    @staticmethod
    def _get_endpoint_url(*args, **kwargs):
        endpoint = f"{kwargs['module']}/{kwargs['controller']}/{kwargs['command']}".lower()
        endpoint_params = "/".join(args)
        if endpoint_params:
            return f"{endpoint}/{endpoint_params}"
        return endpoint

    def _get(self, endpoint):
        req_url = f"{self._config.base_url}/{endpoint}"
        response = requests.get(
            req_url,
            verify=self.ssl_verify_cert,
            auth=(self._config.api_key, self._config.api_secret),
            timeout=self._config.timeout,
        )
        return self._process_response(response)

    def _post(self, endpoint, body):
        req_url = f"{self._config.base_url}/{endpoint}"
        response = requests.post(
            req_url,
            json=body,
            verify=self.ssl_verify_cert,
            auth=(self._config.api_key, self._config.api_secret),
            timeout=self._config.timeout,
        )
        return self._process_response(response)

    def execute(self, *args, body=None, **kwargs):
        endpoint = self._get_endpoint_url(*args, **kwargs)
        try:
            if kwargs["method"] == "get":
                return self._get(endpoint)
            elif kwargs["method"] == "post":
                return self._post(endpoint, body=body)
            else:
                raise NotImplementedError(f"Unknown HTTP method: {kwargs['method']}")
        except Exception as e:
            raise APIException(resp_body=e)
