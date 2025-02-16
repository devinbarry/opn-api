from opn_api.api.base import ApiBase


class FirewallFilter(ApiBase):
    """
    Firewall Filter (needs plugin: os-firewall)
    """

    MODULE = "firewall"
    CONTROLLER = "filter"

    def add_rule(self, body=None):
        return self.api(method="post", command="addRule", body=body)

    def del_rule(self, uuid):
        return self.api(uuid, method="post", command="delRule")

    def get_rule(self, uuid):
        return self.api(uuid, method="get", command="getRule")

    def set_rule(self, uuid, body=None):
        return self.api(uuid, method="post", command="setRule", body=body)

    def toggle_rule(self, uuid, body=None):
        return self.api(uuid, method="post", command="toggleRule", body=body)

    def apply(self):
        return self.api(method="post", command="apply")

    def savepoint(self):
        return self.api(method="post", command="savepoint")

    def cancel_rollback(self):
        return self.api(method="post", command="cancelRollback")

    def search_rule(self, body):
        return self.api(method="post", command="searchRule", body=body)


class FirewallAlias(ApiBase):
    MODULE = "firewall"
    CONTROLLER = "alias"
    """
    Firewall Alias Controller
    """

    def add_item(self, *args, body):
        return self.api(*args, method="post", command="addItem", body=body)

    def del_item(self, uuid):
        return self.api(uuid, method="post", command="delItem")

    def export(self, *args):
        return self.api(*args, method="get", command="export")

    def get_detail(self, *args):
        return self.api(*args, method="get", command="get")

    def get_uuid_for_name(self, name):
        return self.api(name, method="get", command="getAliasUUID")

    def get_geo_ip(self, *args):
        return self.api(*args, method="get", command="getGeoIP")

    def get_item(self, uuid):
        return self.api(uuid, method="get", command="getItem")

    def get_table_size(self, *args):
        return self.api(*args, method="get", command="getTableSize")

    def import_(self, *args, body=None):
        return self.api(*args, method="post", command="import", body=body)

    def list_categories(self, *args):
        return self.api(*args, method="get", command="listCategories")

    def list_countries(self, *args):
        return self.api(*args, method="get", command="listCountries")

    def list_network_aliases(self, *args):
        return self.api(*args, method="get", command="listNetworkAliases")

    def list_user_groups(self, *args):
        return self.api(*args, method="get", command="listUserGroups")

    def reconfigure(self):
        return self.api(method="post", command="reconfigure")

    def search_item(self, *args):
        return self.api(*args, method="get", command="searchItem")

    def set(self, *args, body=None):
        return self.api(*args, method="post", command="set", body=body)

    def set_item(self, uuid, body):
        return self.api(uuid, method="post", command="setItem", body=body)

    def toggle_item(self, *args, body=None):
        return self.api(*args, method="post", command="toggleItem", body=body)


class FirewallAliasUtil(ApiBase):
    MODULE = "firewall"
    CONTROLLER = "alias_util"
    """
    Firewall Alias Util
    """

    def add(self, *args, body=None):
        return self.api(*args, method="post", command="add", body=body)

    def list_aliases(self, *args):
        return self.api(*args, method="get", command="aliases")

    def delete(self, *args, body=None):
        return self.api(*args, method="post", command="delete", body=body)

    def find_references(self, *args, body=None):
        return self.api(*args, method="post", command="findReferences", body=body)

    def flush(self, *args, body=None):
        return self.api(*args, method="post", command="flush", body=body)

    def list_alias(self, *args):
        return self.api(*args, method="get", command="list")

    def update_bogons(self, *args):
        return self.api(*args, method="get", command="updateBogons")
