import unittest
from unittest.mock import Mock
from opn_api.client.firewall.filter_controller import FilterController
from opn_api.models.firewall_models import (
    FirewallFilterRule,
    FirewallFilterRuleResponse,
    Action,
    Direction,
    IPProtocol,
    Protocol,
)
from opn_api.exceptions import ParsingError


class TestFilterController(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.filter_controller = FilterController(self.mock_client)
        self.filter_controller.ff = Mock()  # Replace FirewallFilter instance with a Mock

    def test_add_rule(self):
        rule = FirewallFilterRule(
            sequence=10,
            action=Action.PASS,
            quick=True,
            interface=["wan"],
            direction=Direction.IN,
            ipprotocol=IPProtocol.INET,
            protocol=Protocol.TCP,
            source_net="192.168.1.0/24",
            source_not=False,
            destination_net="10.0.0.0/24",
            destination_not=False,
            destination_port="80",
            gateway=None,
            description="Allow HTTP traffic",
            enabled=True,
            log=False
        )
        expected_dict = rule.model_dump(exclude_unset=True)
        self.filter_controller.ff.add_rule.return_value = {'result': 'success'}

        response = self.filter_controller.add_rule(rule)

        self.filter_controller.ff.add_rule.assert_called_once_with(json=expected_dict)
        self.assertEqual(response, {'result': 'success'})

    def test_delete_rule(self):
        self.filter_controller.ff.del_rule.return_value = {'result': 'deleted'}
        response = self.filter_controller.delete_rule("test_uuid")
        self.filter_controller.ff.del_rule.assert_called_once_with("test_uuid")
        self.assertEqual(response, {'result': 'deleted'})

    def test_get_rule_success(self):
        mock_response = {
            'rule': {
                'sequence': '10',
                'action': 'pass',
                'quick': '1',
                'interface': 'wan, lan',
                'direction': 'in',
                'ipprotocol': 'inet',
                'protocol': 'TCP',
                'source_net': '192.168.1.0/24',
                'source_not': '0',
                'source_port': '',
                'destination_net': '10.0.0.0/24',
                'destination_not': '0',
                'destination_port': '80',
                'gateway': '',
                'description': 'Allow HTTP traffic',
                'enabled': '1',
                'log': '0'
            }
        }
        self.filter_controller.ff.get_rule.return_value = mock_response

        expected_rule = FirewallFilterRuleResponse(
            uuid="test_uuid",
            sequence=10,
            action=Action.PASS,
            quick=True,
            interface=["wan", "lan"],
            direction=Direction.IN,
            ipprotocol=IPProtocol.INET,
            protocol=Protocol.TCP,
            source_net="192.168.1.0/24",
            source_not=False,
            source_port="",
            destination_net="10.0.0.0/24",
            destination_not=False,
            destination_port="80",
            gateway="",
            description="Allow HTTP traffic",
            enabled=True,
            log=False
        )

        rule = self.filter_controller.get_rule("test_uuid")
        self.filter_controller.ff.get_rule.assert_called_once_with("test_uuid")
        self.assertEqual(rule, expected_rule)

    def test_get_rule_no_rule_found(self):
        self.filter_controller.ff.get_rule.return_value = {}
        with self.assertRaises(ValueError) as context:
            self.filter_controller.get_rule("non_existent_uuid")
        self.assertIn("No rule found with UUID: non_existent_uuid", str(context.exception))

    def test_get_rule_parsing_error(self):
        mock_response = {
            'rule': {
                'sequence': 'invalid_int',
                # Other fields are omitted for brevity
            }
        }
        self.filter_controller.ff.get_rule.return_value = mock_response
        with self.assertRaises(ParsingError) as context:
            self.filter_controller.get_rule("test_uuid")
        self.assertIn("Failed to parse the rule with UUID: test_uuid", str(context.exception))
        self.assertIn("invalid literal for int() with base 10: 'invalid_int'", str(context.exception))

    def test_set_rule(self):
        rule = FirewallFilterRule(
            sequence=20,
            action=Action.BLOCK,
            quick=False,
            interface=["lan"],
            direction=Direction.OUT,
            ipprotocol=IPProtocol.INET6,
            protocol=Protocol.UDP,
            source_net="10.0.0.0/24",
            source_not=True,
            destination_net="192.168.2.0/24",
            destination_not=True,
            destination_port="53",
            gateway="fe80::1",
            description="Block DNS traffic",
            enabled=False,
            log=True
        )
        expected_dict = rule.model_dump(exclude_unset=True)
        self.filter_controller.ff.set_rule.return_value = {'result': 'updated'}

        response = self.filter_controller.set_rule("test_uuid", rule)

        self.filter_controller.ff.set_rule.assert_called_once_with("test_uuid", json=expected_dict)
        self.assertEqual(response, {'result': 'updated'})

    def test_toggle_rule_enable(self):
        # Initially disabled
        mock_rule = FirewallFilterRuleResponse(
            uuid="test_uuid",
            sequence=30,
            action=Action.REJECT,
            quick=True,
            interface=["dmz"],
            direction=Direction.IN,
            ipprotocol=IPProtocol.INET,
            protocol=Protocol.ICMP,
            source_net="172.16.0.0/16",
            source_not=False,
            source_port=None,
            destination_net="192.168.3.0/24",
            destination_not=False,
            destination_port=None,
            gateway=None,
            description="Reject ICMP traffic",
            enabled=False,
            log=True
        )
        self.filter_controller.get_rule = Mock(return_value=mock_rule)
        self.filter_controller.ff.toggle_rule.return_value = {'result': 'toggled'}

        response = self.filter_controller.toggle_rule("test_uuid")

        self.filter_controller.get_rule.assert_called_once_with("test_uuid")
        self.filter_controller.ff.toggle_rule.assert_called_once_with("test_uuid", json={"enabled": 1})
        self.assertEqual(response, {'result': 'toggled'})

    def test_toggle_rule_disable(self):
        # Initially enabled
        mock_rule = FirewallFilterRuleResponse(
            uuid="test_uuid",
            sequence=40,
            action=Action.PASS,
            quick=False,
            interface=["wan"],
            direction=Direction.OUT,
            ipprotocol=IPProtocol.INET6,
            protocol=Protocol.ANY,
            source_net="0.0.0.0/0",
            source_not=False,
            source_port=None,
            destination_net="0.0.0.0/0",
            destination_not=False,
            destination_port=None,
            gateway=None,
            description="Allow all traffic",
            enabled=True,
            log=False
        )
        self.filter_controller.get_rule = Mock(return_value=mock_rule)
        self.filter_controller.ff.toggle_rule.return_value = {'result': 'toggled'}

        response = self.filter_controller.toggle_rule("test_uuid")

        self.filter_controller.get_rule.assert_called_once_with("test_uuid")
        self.filter_controller.ff.toggle_rule.assert_called_once_with("test_uuid", json={"enabled": 0})
        self.assertEqual(response, {'result': 'toggled'})

    def test_apply_changes(self):
        self.filter_controller.ff.apply.return_value = {'result': 'applied'}
        response = self.filter_controller.apply_changes()
        self.filter_controller.ff.apply.assert_called_once()
        self.assertEqual(response, {'result': 'applied'})

    def test_create_savepoint(self):
        self.filter_controller.ff.savepoint.return_value = {'result': 'savepoint_created'}
        response = self.filter_controller.create_savepoint()
        self.filter_controller.ff.savepoint.assert_called_once()
        self.assertEqual(response, {'result': 'savepoint_created'})

    def test_cancel_rollback(self):
        self.filter_controller.ff.cancel_rollback.return_value = {'result': 'rollback_cancelled'}
        response = self.filter_controller.cancel_rollback()
        self.filter_controller.ff.cancel_rollback.assert_called_once()
        self.assertEqual(response, {'result': 'rollback_cancelled'})

    def test_list_rules(self):
        mock_response = {
            'rows': [
                {
                    'uuid': 'rule_uuid_1',
                    'sequence': '10',
                    'action': 'pass',
                    'quick': '1',
                    'interface': 'wan, lan',
                    'direction': 'in',
                    'ipprotocol': 'inet',
                    'protocol': 'TCP',
                    'source_net': '192.168.1.0/24',
                    'source_not': '0',
                    'source_port': '80',
                    'destination_net': '10.0.0.0/24',
                    'destination_not': '0',
                    'destination_port': '443',
                    'gateway': '',
                    'description': 'Allow HTTPS traffic',
                    'enabled': '1',
                    'log': '1'
                },
                {
                    'uuid': 'rule_uuid_2',
                    'sequence': '20',
                    'action': 'block',
                    'quick': '0',
                    'interface': 'dmz',
                    'direction': 'out',
                    'ipprotocol': 'inet6',
                    'protocol': 'UDP',
                    'source_net': '172.16.0.0/16',
                    'source_not': '1',
                    'source_port': '',
                    'destination_net': '192.168.2.0/24',
                    'destination_not': '1',
                    'destination_port': '',
                    'gateway': 'fe80::1',
                    'description': 'Block DNS traffic',
                    'enabled': '0',
                    'log': '0'
                }
            ]
        }
        self.filter_controller.ff.search_rule.return_value = mock_response

        expected_rules = [
            FirewallFilterRuleResponse(
                uuid='rule_uuid_1',
                sequence=10,
                action=Action.PASS,
                quick=True,
                interface=["wan", "lan"],
                direction=Direction.IN,
                ipprotocol=IPProtocol.INET,
                protocol=Protocol.TCP,
                source_net='192.168.1.0/24',
                source_not=False,
                source_port='80',
                destination_net='10.0.0.0/24',
                destination_not=False,
                destination_port='443',
                gateway='',
                description='Allow HTTPS traffic',
                enabled=True,
                log=True
            ),
            FirewallFilterRuleResponse(
                uuid='rule_uuid_2',
                sequence=20,
                action=Action.BLOCK,
                quick=False,
                interface=["dmz"],
                direction=Direction.OUT,
                ipprotocol=IPProtocol.INET6,
                protocol=Protocol.UDP,
                source_net='172.16.0.0/16',
                source_not=True,
                source_port='',
                destination_net='192.168.2.0/24',
                destination_not=True,
                destination_port='',
                gateway='fe80::1',
                description='Block DNS traffic',
                enabled=False,
                log=False
            )
        ]

        rules = self.filter_controller.list_rules()
        self.filter_controller.ff.search_rule.assert_called_once()
        self.assertEqual(rules, expected_rules)

    def test_list_rules_empty(self):
        self.filter_controller.ff.search_rule.return_value = {'rows': []}
        rules = self.filter_controller.list_rules()
        self.filter_controller.ff.search_rule.assert_called_once()
        self.assertEqual(rules, [])

    def test_list_rules_parsing_error(self):
        mock_response = {
            'rows': [
                {
                    'uuid': 'invalid_rule_uuid',
                    'sequence': 'invalid_int',
                    # Other fields are omitted for brevity
                }
            ]
        }
        self.filter_controller.ff.search_rule.return_value = mock_response
        with self.assertRaises(ParsingError) as context:
            self.filter_controller.list_rules()
        self.assertIn("Failed to parse rule in list", str(context.exception))
        self.assertIn("invalid literal for int() with base 10: 'invalid_int'", str(context.exception))

    def test_match_rule_by_attributes_found(self):
        mock_rules = [
            FirewallFilterRuleResponse(
                uuid='rule_uuid_1',
                sequence=10,
                action=Action.PASS,
                quick=True,
                interface=["wan", "lan"],
                direction=Direction.IN,
                ipprotocol=IPProtocol.INET,
                protocol=Protocol.TCP,
                source_net='192.168.1.0/24',
                source_not=False,
                source_port='80',
                destination_net='10.0.0.0/24',
                destination_not=False,
                destination_port='443',
                gateway='',
                description='Allow HTTPS traffic',
                enabled=True,
                log=True
            ),
            FirewallFilterRuleResponse(
                uuid='rule_uuid_2',
                sequence=20,
                action=Action.BLOCK,
                quick=False,
                interface=["dmz"],
                direction=Direction.OUT,
                ipprotocol=IPProtocol.INET6,
                protocol=Protocol.UDP,
                source_net='172.16.0.0/16',
                source_not=True,
                source_port='',
                destination_net='192.168.2.0/24',
                destination_not=True,
                destination_port='',
                gateway='fe80::1',
                description='Block DNS traffic',
                enabled=False,
                log=False
            )
        ]
        self.filter_controller.list_rules = Mock(return_value=mock_rules)

        matched = self.filter_controller.match_rule_by_attributes(action=Action.PASS, enabled=True)
        expected = [
            {
                'uuid': 'rule_uuid_1',
                'sequence': 10,
                'action': Action.PASS,
                'quick': True,
                'interface': ["wan", "lan"],
                'direction': Direction.IN,
                'ipprotocol': IPProtocol.INET,
                'protocol': Protocol.TCP,
                'source_net': '192.168.1.0/24',
                'source_not': False,
                'source_port': '80',
                'destination_net': '10.0.0.0/24',
                'destination_not': False,
                'destination_port': '443',
                'gateway': '',
                'description': 'Allow HTTPS traffic',
                'enabled': True,
                'log': True
            }
        ]
        self.assertEqual(matched, expected)

    def test_match_rule_by_attributes_not_found(self):
        mock_rules = [
            FirewallFilterRuleResponse(
                uuid='rule_uuid_1',
                sequence=10,
                action=Action.PASS,
                quick=True,
                interface=["wan", "lan"],
                direction=Direction.IN,
                ipprotocol=IPProtocol.INET,
                protocol=Protocol.TCP,
                source_net='192.168.1.0/24',
                source_not=False,
                source_port='80',
                destination_net='10.0.0.0/24',
                destination_not=False,
                destination_port='443',
                gateway='',
                description='Allow HTTPS traffic',
                enabled=True,
                log=True
            )
        ]
        self.filter_controller.list_rules = Mock(return_value=mock_rules)

        matched = self.filter_controller.match_rule_by_attributes(action=Action.BLOCK)
        self.assertEqual(matched, [])

    def test_match_rule_by_attributes_partial_match(self):
        mock_rules = [
            FirewallFilterRuleResponse(
                uuid='rule_uuid_1',
                sequence=10,
                action=Action.PASS,
                quick=True,
                interface=["wan", "lan"],
                direction=Direction.IN,
                ipprotocol=IPProtocol.INET,
                protocol=Protocol.TCP,
                source_net='192.168.1.0/24',
                source_not=False,
                source_port='80',
                destination_net='10.0.0.0/24',
                destination_not=False,
                destination_port='443',
                gateway='',
                description='Allow HTTPS traffic',
                enabled=True,
                log=True
            ),
            FirewallFilterRuleResponse(
                uuid='rule_uuid_2',
                sequence=20,
                action=Action.BLOCK,
                quick=False,
                interface=["dmz"],
                direction=Direction.OUT,
                ipprotocol=IPProtocol.INET6,
                protocol=Protocol.UDP,
                source_net='172.16.0.0/16',
                source_not=True,
                source_port='',
                destination_net='192.168.2.0/24',
                destination_not=True,
                destination_port='',
                gateway='fe80::1',
                description='Block DNS traffic',
                enabled=False,
                log=False
            )
        ]
        self.filter_controller.list_rules = Mock(return_value=mock_rules)

        matched = self.filter_controller.match_rule_by_attributes(direction=Direction.OUT, protocol=Protocol.UDP)
        expected = [
            {
                'uuid': 'rule_uuid_2',
                'sequence': 20,
                'action': Action.BLOCK,
                'quick': False,
                'interface': ["dmz"],
                'direction': Direction.OUT,
                'ipprotocol': IPProtocol.INET6,
                'protocol': Protocol.UDP,
                'source_net': '172.16.0.0/16',
                'source_not': True,
                'source_port': '',
                'destination_net': '192.168.2.0/24',
                'destination_not': True,
                'destination_port': '',
                'gateway': 'fe80::1',
                'description': 'Block DNS traffic',
                'enabled': False,
                'log': False
            }
        ]
        self.assertEqual(matched, expected)
