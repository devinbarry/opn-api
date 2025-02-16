from opn_api.api.client import OPNAPIClient


class ApiBase:
    def __init__(self, api_client: OPNAPIClient):
        self._api_client = api_client
        self.module = self.MODULE
        self.controller = self.CONTROLLER

    def api(self, *args, method, command, body=None, **kwargs):
        return self._api_client.execute(
            *args, module=self.module, controller=self.controller, method=method, command=command, body=body, **kwargs
        )
