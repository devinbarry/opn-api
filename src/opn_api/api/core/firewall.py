from opn_api.api.base import ApiBase


class FirewallFilter(ApiBase):
    MODULE = "firewall"
    CONTROLLER = "filter"
    """
    Firewall Filter (needs plugin: os-firewall)
    """

    def add_rule(self, *args, json=None):
        return self.api(*args, method="post", command="addRule", json=json)

    def del_rule(self, *args):
        return self.api(*args, method="post", command="delRule")

    def get_rule(self, *args):
        return self.api(*args, method="get", command="getRule")

    def set_rule(self, *args):
        return self.api(*args, method="post", command="setRule")

    def apply(self, *args):
        return self.api(*args, method="post", command="apply")

    def savepoint(self, *args):
        return self.api(*args, method="post", command="savepoint")

    def cancel_rollback(self, *args):
        return self.api(*args, method="post", command="cancelRollback")

    def get(self, *args):
        return self.api(*args, method="get", command="get")


class FirewallAlias(ApiBase):
    MODULE = "firewall"
    CONTROLLER = "alias"
    """
    Firewall Alias Util
    """

    def add_item(self, *args, body):
        return self.api(*args, method="post", command="addItem", json=body)

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

    def import_(self, *args, json=None):
        return self.api(*args, method="post", command="import", json=json)

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

    def search_item(self, *args, **kwargs):
        return self.api(*args, method="get", command="searchItem", **kwargs)

    def set(self, *args, json=None):
        return self.api(*args, method="post", command="set", json=json)

    def set_item(self, uuid, body):
        return self.api(uuid, method="post", command="setItem", json=body)

    def toggle_item(self, *args, json=None):
        return self.api(*args, method="post", command="toggleItem", json=json)


class FirewallAliasUtil(ApiBase):
    MODULE = "firewall"
    CONTROLLER = "alias_util"
    """
    Firewall Alias Util
    """

    def add(self, *args, json=None):
        return self.api(*args, method="post", command="add", json=json)

    def list_aliases(self, *args):
        return self.api(*args, method="get", command="aliases")

    def delete(self, *args, json=None):
        return self.api(*args, method="post", command="delete", json=json)

    def find_references(self, *args, json=None):
        return self.api(*args, method="post", command="findReferences", json=json)

    def flush(self, *args, json=None):
        return self.api(*args, method="post", command="flush", json=json)

    def list_alias(self, *args):
        return self.api(*args, method="get", command="list")

    def update_bogons(self, *args):
        return self.api(*args, method="get", command="updateBogons")
