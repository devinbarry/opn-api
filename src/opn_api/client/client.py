from .controllers.alias_controller import AliasController
from .controllers.filter_controller import FilterController


class OPNFirewallClient:
    def __init__(self, client):
        self.client = client
        self._alias = AliasController(self.client)
        self._filter = FilterController(self.client)

    @property
    def alias(self) -> AliasController:
        return self._alias

    @property
    def filter(self) -> FilterController:
        return self._filter
