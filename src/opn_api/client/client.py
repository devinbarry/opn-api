from .firewall.alias_controller import Alias
from .firewall.filter_controller import Filter


class Firewall:

    def __init__(self, client):
        self.client = client
        self._alias = Alias(self.client)
        self._filter = Filter(self.client)

    @property
    def alias(self) -> Alias:
        return self._alias

    @property
    def filter(self) -> Filter:
        return self._filter
