from opn_api.api.base import ApiBase


class Service(ApiBase):
    """
    Syslog ServiceController
    """

    MODULE = "syslog"
    CONTROLLER = "service"

    def reconfigure(self, *args):
        return self.api(*args, method="post", command="reconfigure")

    def stats(self, *args):
        return self.api(*args, method="get", command="stats")


class Settings(ApiBase):
    """
    Syslog SettingsController
    """

    MODULE = "syslog"
    CONTROLLER = "settings"

    def add_destination(self, *args):
        return self.api(*args, method="post", command="addDestination")

    def del_destination(self, *args):
        return self.api(*args, method="post", command="delDestination")

    def get(self, *args):
        return self.api(*args, method="get", command="get")

    def set_destination(self, *args):
        return self.api(*args, method="post", command="setDestination")
