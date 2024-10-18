import unittest
from unittest.mock import Mock, patch
from opn_api.client.client import OPNFirewallClient
from opn_api.client.firewall.alias_controller import AliasController
from opn_api.client.firewall.filter_controller import FilterController


class TestOPNFirewallClient(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.opn_client = OPNFirewallClient(self.mock_client)

    def test_initialization(self):
        # Verify that AliasController and FilterController are instantiated with the mock client
        with (patch('opn_api.client.client.AliasController') as MockAliasController,
              patch('opn_api.client.client.FilterController') as MockFilterController):
            OPNFirewallClient(self.mock_client)

            MockAliasController.assert_called_once_with(self.mock_client)
            MockFilterController.assert_called_once_with(self.mock_client)

    def test_alias_property(self):
        # Verify that the alias property returns an instance of AliasController
        self.assertIsInstance(self.opn_client.alias, AliasController)

    def test_filter_property(self):
        # Verify that the filter property returns an instance of FilterController
        self.assertIsInstance(self.opn_client.filter, FilterController)

    def test_alias_and_filter_are_singleton(self):
        # Ensure that multiple accesses to alias and filter return the same instances
        alias_first = self.opn_client.alias
        alias_second = self.opn_client.alias
        filter_first = self.opn_client.filter
        filter_second = self.opn_client.filter

        self.assertIs(alias_first, alias_second)
        self.assertIs(filter_first, filter_second)

    def test_alias_controller_methods(self):
        # Example: Test that alias controller methods are callable
        self.opn_client.alias.list = Mock(return_value=[])
        result = self.opn_client.alias.list()
        self.opn_client.alias.list.assert_called_once()
        self.assertEqual(result, [])

    def test_filter_controller_methods(self):
        # Example: Test that filter controller methods are callable
        self.opn_client.filter.list_rules = Mock(return_value=[])
        result = self.opn_client.filter.list_rules()
        self.opn_client.filter.list_rules.assert_called_once()
        self.assertEqual(result, [])
