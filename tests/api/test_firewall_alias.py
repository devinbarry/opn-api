import unittest
from unittest.mock import patch, MagicMock
from opn_api.api.core.firewall import FirewallAlias
from opn_api.api.client import ApiClient
from ..mocks.alias import *


class TestFirewallAlias(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock(spec=ApiClient)
        self.firewall_alias = FirewallAlias(self.mock_client)

    @patch('opn_api.api.core.firewall.ApiBase._api_call')
    def test_export(self, mock_api_call):
        mock_api_call.return_value = mock_export_data()
        result = self.firewall_alias.export()
        self.assertEqual(result, mock_export_data())
        mock_api_call.assert_called_once()

    @patch('opn_api.api.core.firewall.ApiBase._api_call')
    def test_get_detail(self, mock_api_call):
        mock_api_call.return_value = mock_get_detail_data()
        result = self.firewall_alias.get_detail()
        self.assertEqual(result, mock_get_detail_data())
        mock_api_call.assert_called_once()

    def test_get_uuid_for_name(self):
        name = "test_alias"
        self.mock_client.execute.return_value = mock_get_uuid_for_name_data(name)
        result = self.firewall_alias.get_uuid_for_name(name)
        self.assertEqual(result, mock_get_uuid_for_name_data(name))
        self.mock_client.execute.assert_called_once_with(
            name, module='firewall', controller='alias', method='get', command='getAliasUUID')

    @patch('opn_api.api.core.firewall.ApiBase._api_call')
    def test_get_geo_ip(self, mock_api_call):
        mock_api_call.return_value = mock_get_geo_ip_data()
        result = self.firewall_alias.get_geo_ip()
        self.assertEqual(result, mock_get_geo_ip_data())
        mock_api_call.assert_called_once()

    def test_get_item(self):
        uuid = "test_uuid"
        self.mock_client.execute.return_value = mock_get_item_data(uuid)
        result = self.firewall_alias.get_item(uuid)
        self.assertEqual(result, mock_get_item_data(uuid))
        self.mock_client.execute.assert_called_once_with(
            uuid, module='firewall', controller='alias', method='get', command='getItem')

    @patch('opn_api.api.core.firewall.ApiBase._api_call')
    def test_get_table_size(self, mock_api_call):
        mock_api_call.return_value = mock_get_table_size_data()
        result = self.firewall_alias.get_table_size()
        self.assertEqual(result, mock_get_table_size_data())
        mock_api_call.assert_called_once()

    @patch('opn_api.api.core.firewall.ApiBase._api_call')
    def test_list_categories(self, mock_api_call):
        mock_api_call.return_value = mock_list_categories_data()
        result = self.firewall_alias.list_categories()
        self.assertEqual(result, mock_list_categories_data())
        mock_api_call.assert_called_once()

    @patch('opn_api.api.core.firewall.ApiBase._api_call')
    def test_list_countries(self, mock_api_call):
        mock_api_call.return_value = mock_list_countries_data()
        result = self.firewall_alias.list_countries()
        self.assertEqual(result, mock_list_countries_data())
        mock_api_call.assert_called_once()

    @patch('opn_api.api.core.firewall.ApiBase._api_call')
    def test_list_network_aliases(self, mock_api_call):
        mock_api_call.return_value = mock_list_network_aliases_data()
        result = self.firewall_alias.list_network_aliases()
        self.assertEqual(result, mock_list_network_aliases_data())
        mock_api_call.assert_called_once()

    @patch('opn_api.api.core.firewall.ApiBase._api_call')
    def test_list_user_groups(self, mock_api_call):
        mock_api_call.return_value = mock_list_user_groups_data()
        result = self.firewall_alias.list_user_groups()
        self.assertEqual(result, mock_list_user_groups_data())
        mock_api_call.assert_called_once()

    @patch('opn_api.api.core.firewall.ApiBase._api_call')
    def test_search_item(self, mock_api_call):
        mock_api_call.return_value = mock_search_item_data()
        result = self.firewall_alias.search_item()
        self.assertEqual(result, mock_search_item_data())
        mock_api_call.assert_called_once()

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
            uuid, module='firewall', controller='alias', method='post', command='delItem')

    @patch('opn_api.api.core.firewall.ApiBase._api_call')
    def test_import(self, mock_api_call):
        json_data = {"key": "value"}
        mock_api_call.return_value = mock_import_data()
        result = self.firewall_alias.import_(json=json_data)
        self.assertEqual(result, mock_import_data())
        mock_api_call.assert_called_once()

    def test_reconfigure(self):
        self.mock_client.execute.return_value = mock_reconfigure_data()
        result = self.firewall_alias.reconfigure()
        self.assertEqual(result, mock_reconfigure_data())
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='alias', method='post', command='reconfigure')

    @patch('opn_api.api.core.firewall.ApiBase._api_call')
    def test_set(self, mock_api_call):
        json_data = {"key": "value"}
        mock_api_call.return_value = mock_set_data()
        result = self.firewall_alias.set(json=json_data)
        self.assertEqual(result, mock_set_data())
        mock_api_call.assert_called_once()

    def test_set_item(self):
        uuid = "test_uuid"
        body = {"key": "value"}
        self.mock_client.execute.return_value = mock_set_item_data()
        result = self.firewall_alias.set_item(uuid, body)
        self.assertEqual(result, mock_set_item_data())
        self.mock_client.execute.assert_called_once_with(
            uuid, module='firewall', controller='alias', method='post', command='setItem', json=body)

    @patch('opn_api.api.core.firewall.ApiBase._api_call')
    def test_toggle_item(self, mock_api_call):
        json_data = {"key": "value"}
        mock_api_call.return_value = mock_toggle_item_data()
        result = self.firewall_alias.toggle_item(json=json_data)
        self.assertEqual(result, mock_toggle_item_data())
        mock_api_call.assert_called_once()

