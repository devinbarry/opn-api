from opn_api.api.base import ApiBase


class Gateway(ApiBase):
    """
    Routes GatewayController
    """

    MODULE = "routes"
    CONTROLLER = "gateway"

    def status(self, *args):
        return self.api(*args, method="get", command="status")


class Routes(ApiBase):
    """
    Routes RoutesController
    """

    MODULE = "routes"
    CONTROLLER = "routes"

    def add_route(self, *args):
        return self.api(*args, method="post", command="addroute")

    def del_route(self, *args):
        return self.api(*args, method="post", command="delroute")

    def get(self, *args):
        return self.api(*args, method="get", command="get")

    def reconfigure(self, *args):
        return self.api(*args, method="post", command="reconfigure")

    def set_route(self, *args):
        return self.api(*args, method="post", command="setroute")
