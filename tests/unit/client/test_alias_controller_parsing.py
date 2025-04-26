import unittest
from unittest.mock import Mock
from pydantic import ValidationError
from opn_api.models.firewall_alias import AliasType
from opn_api.client.controllers import AliasController


class TestAliasControllerParseMethod(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.alias = AliasController(self.mock_client)

    def test_parse_alias_type_variations(self):
        # Test different type formats
        test_cases = [
            ("Host(s)", AliasType.HOST),
            ("Network(s)", AliasType.NETWORK),
            ("host", AliasType.HOST),
            ("NETWORK", AliasType.NETWORK),
            ("Port(s)", AliasType.PORT),
            ("GeoIP", AliasType.GEOIP),
        ]

        for input_type, expected_type in test_cases:
            with self.subTest(input_type=input_type):
                alias_data = {"uuid": "test_uuid", "name": "test_alias", "type": input_type, "enabled": "1"}
                result = self.alias._parse_alias_search_item(alias_data)
                self.assertEqual(result.type, expected_type)

    def test_parse_alias_enabled_variations(self):
        # Test different enabled values
        test_cases = [
            ("1", True),
            ("0", False),
            (1, True),
            (0, False),
        ]

        for input_enabled, expected_enabled in test_cases:
            with self.subTest(input_enabled=input_enabled):
                alias_data = {"uuid": "test_uuid", "name": "test_alias", "type": "host", "enabled": input_enabled}
                result = self.alias._parse_alias_search_item(alias_data)
                self.assertEqual(result.enabled, expected_enabled)

    def test_parse_alias_content_variations(self):
        # Test different content formats
        test_cases = [
            # Single line content
            ("192.168.1.1", ["192.168.1.1"]),
            # Multiple line content
            ("192.168.1.1\n192.168.1.2", ["192.168.1.1", "192.168.1.2"]),
            # Empty content
            ("", []),
            # Content with whitespace
            ("192.168.1.1\n  192.168.1.2  ", ["192.168.1.1", "  192.168.1.2  "]),
        ]

        for input_content, expected_content in test_cases:
            with self.subTest(input_content=input_content):
                alias_data = {
                    "uuid": "test_uuid",
                    "name": "test_alias",
                    "type": "host",
                    "enabled": "1",
                    "content": input_content,
                }
                result = self.alias._parse_alias_search_item(alias_data)
                self.assertEqual(result.content, expected_content)

    def test_parse_alias_optional_fields(self):
        # Test with all optional fields
        full_alias_data = {
            "uuid": "test_uuid",
            "name": "test_alias",
            "type": "host",
            "enabled": "1",
            "description": "Test description",
            "update_freq": "30",
            "counters": "enable",
            "proto": "IPv4",
        }
        result = self.alias._parse_alias_search_item(full_alias_data)
        self.assertEqual(result.description, "Test description")
        self.assertEqual(result.update_freq, "30")
        self.assertEqual(result.counters, "enable")

        # Test with minimal required fields
        minimal_alias_data = {"uuid": "test_uuid", "name": "test_alias", "type": "host", "enabled": "1"}
        result = self.alias._parse_alias_search_item(minimal_alias_data)
        self.assertEqual(result.description, "")
        self.assertEqual(result.update_freq, "")
        self.assertEqual(result.counters, "")
        self.assertEqual(result.content, [])

    def test_parse_alias_validation_errors(self):
        # Test missing required field (name)
        with self.assertRaises(ValidationError):
            alias_data = {"uuid": "test_uuid", "type": "host", "enabled": "1"}
            self.alias._parse_alias_search_item(alias_data)

        # Test invalid type
        with self.assertRaises(ValueError):
            alias_data = {"uuid": "test_uuid", "name": "test_alias", "type": "invalid_type", "enabled": "1"}
            self.alias._parse_alias_search_item(alias_data)

        # Test invalid enabled value
        with self.assertRaises(ValueError):
            alias_data = {"uuid": "test_uuid", "name": "test_alias", "type": "host", "enabled": "invalid"}
            self.alias._parse_alias_search_item(alias_data)

    def test_list_with_various_types(self):
        # Test list method with various alias types
        mock_response = {
            "rows": [
                {"uuid": "uuid1", "name": "host_alias", "type": "Host(s)", "enabled": "1"},
                {"uuid": "uuid2", "name": "network_alias", "type": "Network(s)", "enabled": "0"},
                {"uuid": "uuid3", "name": "port_alias", "type": "Port(s)", "content": "80\n443", "enabled": "1"},
            ]
        }
        self.alias.fa.search_item = Mock(return_value=mock_response)
        result = self.alias.list()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].type, AliasType.HOST)
        self.assertEqual(result[1].type, AliasType.NETWORK)
        self.assertEqual(result[2].type, AliasType.PORT)
        self.assertTrue(result[0].enabled)
        self.assertFalse(result[1].enabled)
        self.assertEqual(result[2].content, ["80", "443"])
