import unittest
from unittest.mock import MagicMock
from opn_api.api.core.firewall import FirewallFilter
from opn_api.api.client import OPNAPIClient


class TestFirewallFilter(unittest.TestCase):

    def setUp(self):
        self.mock_client = MagicMock(spec=OPNAPIClient)
        self.firewall_filter = FirewallFilter(self.mock_client)

    def test_add_rule(self):
        body = {'rule': 'some_rule_data'}
        self.mock_client.execute.return_value = {'result': 'success'}
        result = self.firewall_filter.add_rule(body=body)
        self.assertEqual(result, {'result': 'success'})
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='filter', method='post', command='addRule', body=body
        )

    def test_del_rule(self):
        uuid = 'test_uuid'
        self.mock_client.execute.return_value = {'result': 'deleted'}
        result = self.firewall_filter.del_rule(uuid)
        self.assertEqual(result, {'result': 'deleted'})
        self.mock_client.execute.assert_called_once_with(
            uuid, module='firewall', controller='filter', method='post', command='delRule', body=None
        )

    def test_get_rule(self):
        uuid = 'test_uuid'
        self.mock_client.execute.return_value = {'rule': 'some_rule_data'}
        result = self.firewall_filter.get_rule(uuid)
        self.assertEqual(result, {'rule': 'some_rule_data'})
        self.mock_client.execute.assert_called_once_with(
            uuid, module='firewall', controller='filter', method='get', command='getRule', body=None
        )

    def test_set_rule(self):
        uuid = 'test_uuid'
        body = {'rule': 'updated_rule_data'}
        self.mock_client.execute.return_value = {'result': 'updated'}
        result = self.firewall_filter.set_rule(uuid, body=body)
        self.assertEqual(result, {'result': 'updated'})
        self.mock_client.execute.assert_called_once_with(
            uuid, module='firewall', controller='filter', method='post', command='setRule', body=body
        )

    def test_toggle_rule(self):
        uuid = 'test_uuid'
        body = {'enabled': '1'}
        self.mock_client.execute.return_value = {'result': 'toggled'}
        result = self.firewall_filter.toggle_rule(uuid, body=body)
        self.assertEqual(result, {'result': 'toggled'})
        self.mock_client.execute.assert_called_once_with(
            uuid, module='firewall', controller='filter', method='post', command='toggleRule', body=body
        )

    def test_apply(self):
        self.mock_client.execute.return_value = {'result': 'applied'}
        result = self.firewall_filter.apply()
        self.assertEqual(result, {'result': 'applied'})
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='filter', method='post', command='apply', body=None
        )

    def test_savepoint(self):
        self.mock_client.execute.return_value = {'result': 'savepoint_created'}
        result = self.firewall_filter.savepoint()
        self.assertEqual(result, {'result': 'savepoint_created'})
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='filter', method='post', command='savepoint', body=None
        )

    def test_cancel_rollback(self):
        self.mock_client.execute.return_value = {'result': 'rollback_cancelled'}
        result = self.firewall_filter.cancel_rollback()
        self.assertEqual(result, {'result': 'rollback_cancelled'})
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='filter', method='post', command='cancelRollback', body=None
        )

    def test_search_rule(self):
        body = {'search_param': 'value'}
        self.mock_client.execute.return_value = {'rules': []}
        result = self.firewall_filter.search_rule(body=body)
        self.assertEqual(result, {'rules': []})
        self.mock_client.execute.assert_called_once_with(
            module='firewall', controller='filter', method='post', command='searchRule', body=body
        )
