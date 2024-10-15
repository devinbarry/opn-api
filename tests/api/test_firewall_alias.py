import unittest
from unittest.mock import MagicMock
from opn_api.api.core.firewall import FirewallAlias
from opn_api.api.client import ApiClient
from tests.mocks.alias import *


class TestFirewallAlias(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock(spec=ApiClient)
        self.firewall_alias = FirewallAlias(self.mock_client)

    def test_export(self):
        self.mock_client.execute.return_value = mock_export_data()
        result = self.firewall_alias.export()
        self.assertEqual(result, mock_export_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='get', command='export', json=None
        )

    def test_get_detail(self):
        self.mock_client.execute.return_value = mock_get_detail_data()
        result = self.firewall_alias.get_detail()
        self.assertEqual(result, mock_get_detail_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='get', command='get', json=None
        )

    def test_get_uuid_for_name(self):
        name = "test_alias"
        self.mock_client.execute.return_value = mock_get_uuid_for_name_data(name)
        result = self.firewall_alias.get_uuid_for_name(name)
        self.assertEqual(result, mock_get_uuid_for_name_data(name))
        self.mock_client.execute.assert_called_once_with(
            name, module='firewall', controller='alias', method='get', command='getAliasUUID', json=None)

    def test_get_geo_ip(self):
        self.mock_client.execute.return_value = mock_get_geo_ip_data()
        result = self.firewall_alias.get_geo_ip()
        self.assertEqual(result, mock_get_geo_ip_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='get', command='getGeoIP', json=None
        )

    def test_get_item(self):
        uuid = "test_uuid"
        self.mock_client.execute.return_value = mock_get_item_data(uuid)
        result = self.firewall_alias.get_item(uuid)
        self.assertEqual(result, mock_get_item_data(uuid))
        self.mock_client.execute.assert_called_once_with(
            uuid, module='firewall', controller='alias', method='get', command='getItem', json=None)

    def test_get_table_size(self):
        self.mock_client.execute.return_value = mock_get_table_size_data()
        result = self.firewall_alias.get_table_size()
        self.assertEqual(result, mock_get_table_size_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='get', command='getTableSize', json=None
        )

    def test_list_categories(self):
        self.mock_client.execute.return_value = mock_list_categories_data()
        result = self.firewall_alias.list_categories()
        self.assertEqual(result, mock_list_categories_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='get', command='listCategories', json=None
        )

    def test_list_countries(self):
        self.mock_client.execute.return_value = mock_list_countries_data()
        result = self.firewall_alias.list_countries()
        self.assertEqual(result, mock_list_countries_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='get', command='listCountries', json=None
        )

    def test_list_network_aliases(self):
        self.mock_client.execute.return_value = mock_list_network_aliases_data()
        result = self.firewall_alias.list_network_aliases()
        self.assertEqual(result, mock_list_network_aliases_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='get', command='listNetworkAliases', json=None
        )

    def test_list_user_groups(self):
        self.mock_client.execute.return_value = mock_list_user_groups_data()
        result = self.firewall_alias.list_user_groups()
        self.assertEqual(result, mock_list_user_groups_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='get', command='listUserGroups', json=None
        )

    def test_search_item(self):
        self.mock_client.execute.return_value = mock_search_item_data()
        result = self.firewall_alias.search_item()
        self.assertEqual(result, mock_search_item_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='get', command='searchItem', json=None
        )

    def test_add_item(self):
        args = ("arg1", "arg2")
        body = {"key": "value"}
        self.mock_client.execute.return_value = mock_add_item_data()
        result = self.firewall_alias.add_item(*args, body=body)
        self.assertEqual(result, mock_add_item_data())
        self.mock_client.execute.assert_called_once_with(
            *args, module='firewall', controller='alias', method='post', command='addItem', json=body)

    def test_del_item(self):
        uuid = "test_uuid"
        self.mock_client.execute.return_value = mock_del_item_data()
        result = self.firewall_alias.del_item(uuid)
        self.assertEqual(result, mock_del_item_data())
        self.mock_client.execute.assert_called_once_with(
            uuid, module='firewall', controller='alias', method='post', command='delItem', json=None)

    def test_import(self):
        json_data = {"key": "value"}
        self.mock_client.execute.return_value = mock_import_data()
        result = self.firewall_alias.import_(json=json_data)
        self.assertEqual(result, mock_import_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='post', command='import', json=json_data
        )

    def test_reconfigure(self):
        self.mock_client.execute.return_value = mock_reconfigure_data()
        result = self.firewall_alias.reconfigure()
        self.assertEqual(result, mock_reconfigure_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='post', command='reconfigure', json=None)

    def test_set(self):
        json_data = {"key": "value"}
        self.mock_client.execute.return_value = mock_set_data()
        result = self.firewall_alias.set(json=json_data)
        self.assertEqual(result, mock_set_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='post', command='set', json=json_data
        )

    def test_set_item(self):
        uuid = "test_uuid"
        body = {"key": "value"}
        self.mock_client.execute.return_value = mock_set_item_data()
        result = self.firewall_alias.set_item(uuid, body)
        self.assertEqual(result, mock_set_item_data())
        self.mock_client.execute.assert_called_once_with(
            uuid, module='firewall', controller='alias', method='post', command='setItem', json=body)

    def test_toggle_item(self):
        json_data = {"key": "value"}
        self.mock_client.execute.return_value = mock_toggle_item_data()
        result = self.firewall_alias.toggle_item(json=json_data)
        self.assertEqual(result, mock_toggle_item_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='post', command='toggleItem', json=json_data
        )
