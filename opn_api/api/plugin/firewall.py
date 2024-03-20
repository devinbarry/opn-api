from opn_api.api.base import ApiBase


class FirewallFilter(ApiBase):
    MODULE = "firewall"
    CONTROLLER = "filter"
    """
    Firewall Filter (needs plugin: os-firewall)
    """

    @ApiBase._api_call
    def add_rule(self, *args, json=None):
        self.method = "post"
        self.command = "addRule"

    @ApiBase._api_call
    def del_rule(self, *args):
        self.method = "post"
        self.command = "delRule"

    @ApiBase._api_call
    def get_rule(self, *args):
        self.method = "get"
        self.command = "getRule"

    @ApiBase._api_call
    def set_rule(self, *args):
        self.method = "post"
        self.command = "setRule"

    @ApiBase._api_call
    def apply(self, *args):
        self.method = "post"
        self.command = "apply"

    @ApiBase._api_call
    def savepoint(self, *args):
        self.method = "post"
        self.command = "savepoint"

    @ApiBase._api_call
    def cancel_rollback(self, *args):
        self.method = "post"
        self.command = "cancelRollback"

    @ApiBase._api_call
    def get(self, *args):
        self.method = "get"
        self.command = "get"


class FirewallAlias(ApiBase):
    MODULE = "firewall"
    CONTROLLER = "alias"
    """
    Firewall Alias Util
    """

    def add_item(self, *args, body):
        self.method = "post"
        self.command = "addItem"
        self.api(*args, json=body)

    def del_item(self, uuid):
        self.method = "post"
        self.command = "delItem"
        return self.api(uuid)

    @ApiBase._api_call
    def export(self, *args):
        self.method = "get"
        self.command = "export"

    @ApiBase._api_call
    def get_detail(self, *args):
        self.method = "get"
        self.command = "get"

    def get_uuid_for_name(self, name):
        self.method = "get"
        self.command = "getAliasUUID"
        return self.api(name)

    @ApiBase._api_call
    def get_geo_ip(self, *args):
        self.method = "get"
        self.command = "getGeoIP"

    def get_item(self, uuid):
        self.method = "get"
        self.command = "getItem"
        return self.api(uuid)

    @ApiBase._api_call
    def get_table_size(self, *args):
        self.method = "get"
        self.command = "getTableSize"

    @ApiBase._api_call
    def import_(self, *args, json=None):
        self.method = "post"
        self.command = "import"

    @ApiBase._api_call
    def list_categories(self, *args):
        self.method = "get"
        self.command = "listCategories"

    @ApiBase._api_call
    def list_countries(self, *args):
        self.method = "get"
        self.command = "listCountries"

    @ApiBase._api_call
    def list_network_aliases(self, *args):
        self.method = "get"
        self.command = "listNetworkAliases"

    @ApiBase._api_call
    def list_user_groups(self, *args):
        self.method = "get"
        self.command = "listUserGroups"

    def reconfigure(self):
        self.method = "post"
        self.command = "reconfigure"
        return self.api()

    @ApiBase._api_call
    def search_item(self, *args, **kwargs):
        self.method = "get"
        self.command = "searchItem"

    @ApiBase._api_call
    def set(self, *args, json=None):
        self.method = "post"
        self.command = "set"

    def set_item(self, uuid, body):
        self.method = "post"
        self.command = "setItem"
        return self.api(uuid, json=body)

    @ApiBase._api_call
    def toggle_item(self, *args, json=None):
        self.method = "post"
        self.command = "toggleItem"


class FirewallAliasUtil(ApiBase):
    MODULE = "firewall"
    CONTROLLER = "alias_util"
    """
    Firewall Alias Util
    """

    @ApiBase._api_call
    def add(self, *args, json=None):
        self.method = "post"
        self.command = "add"

    @ApiBase._api_call
    def list_aliases(self, *args):
        self.method = "get"
        self.command = "aliases"

    @ApiBase._api_call
    def delete(self, *args, json=None):
        self.method = "post"
        self.command = "delete"

    @ApiBase._api_call
    def find_references(self, *args, json=None):
        self.method = "post"
        self.command = "findReferences"

    @ApiBase._api_call
    def flush(self, *args, json=None):
        self.method = "post"
        self.command = "flush"

    @ApiBase._api_call
    def list_alias(self, *args):
        self.method = "get"
        self.command = "list"

    @ApiBase._api_call
    def update_bogons(self, *args):
        self.method = "get"
        self.command = "updateBogons"

