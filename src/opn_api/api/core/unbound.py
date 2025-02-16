from opn_api.api.base import ApiBase


class Service(ApiBase):
    """
    Unbound ServiceController
    """

    MODULE = "unbound"
    CONTROLLER = "service"

    def reconfigure(self, *args):
        return self.api(*args, method="post", command="reconfigure")


class Settings(ApiBase):
    """
    Unbound SettingsController
    """

    MODULE = "unbound"
    CONTROLLER = "settings"

    def add_domain_override(self, *args):
        return self.api(*args, method="post", command="addDomainOverride")

    def add_host_alias(self, *args):
        return self.api(*args, method="post", command="addHostAlias")

    def add_host_override(self, *args):
        return self.api(*args, method="post", command="addHostOverride")

    def del_domain_override(self, *args):
        return self.api(*args, method="post", command="delDomainOverride")

    def del_host_alias(self, *args):
        return self.api(*args, method="post", command="delHostAlias")

    def del_host_override(self, *args):
        return self.api(*args, method="post", command="delHostOverride")

    def get(self, *args):
        return self.api(*args, method="get", command="get")

    def set_domain_override(self, *args):
        return self.api(*args, method="post", command="setDomainOverride")

    def set_host_alias(self, *args):
        return self.api(*args, method="post", command="setHostAlias")

    def set_host_override(self, *args):
        return self.api(*args, method="post", command="setHostOverride")
