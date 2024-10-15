from opn_api.api.base import ApiBase


class General(ApiBase):
    MODULE = "nodeexporter"
    CONTROLLER = "general"
    """
    Nodeexporter GeneralController
    """

    def get(self, *args):
        return self.api(*args, method="get", command="get")

    def set(self, *args):
        return self.api(*args, method="post", command="set")


class Service(ApiBase):
    MODULE = "nodeexporter"
    CONTROLLER = "service"
    """
    Nodeexporter ServiceController
    """

    def reconfigure(self, *args):
        return self.api(*args, method="post", command="reconfigure")
