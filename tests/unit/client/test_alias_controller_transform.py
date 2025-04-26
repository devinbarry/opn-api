import unittest
from unittest.mock import Mock
from pydantic import ValidationError
from opn_api.models.firewall_alias import (
    AliasType,
    ProtocolType,
    FirewallAliasResponse,
)
from opn_api.exceptions import ParsingError
from opn_api.client.firewall import AliasController


class TestAliasControllerTransform(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.alias = AliasController(self.mock_client)
        self.test_uuid = "test-uuid-1234"

    def test_transform_alias_response_full(self):
        """Test transformation of a complete alias response"""
        input_data = {
            "name": "test_alias",
            "description": "Test description",
            "type": {"host": {"selected": 1}},
            "proto": {"IPv4": {"selected": 1}},
            "content": {
                "192.168.1.1": {"selected": 1, "value": "192.168.1.1"},
                "192.168.1.2": {"selected": 1, "value": "192.168.1.2"},
            },
            "enabled": "1",
            "updatefreq": "60",
            "counters": "enable",
        }

        result = self.alias._transform_alias_response(self.test_uuid, input_data)

        self.assertIsInstance(result, FirewallAliasResponse)
        self.assertEqual(result.uuid, self.test_uuid)
        self.assertEqual(result.name, "test_alias")
        self.assertEqual(result.description, "Test description")
        self.assertEqual(result.type, AliasType.HOST)
        self.assertEqual(result.proto, ProtocolType.IPV4)
        self.assertEqual(result.content, ["192.168.1.1", "192.168.1.2"])
        self.assertTrue(result.enabled)
        self.assertEqual(result.update_freq, "60")
        self.assertEqual(result.counters, "enable")

    def test_transform_alias_response_minimal(self):
        """Test transformation with minimal required fields"""
        input_data = {
            "name": "test_alias",
            "type": {"host": {"selected": 1}},
        }

        result = self.alias._transform_alias_response(self.test_uuid, input_data)

        self.assertEqual(result.uuid, self.test_uuid)
        self.assertEqual(result.name, "test_alias")
        self.assertEqual(result.description, "")
        self.assertEqual(result.type, AliasType.HOST)
        self.assertIsNone(result.proto)
        self.assertEqual(result.content, [])
        self.assertTrue(result.enabled)  # default value
        self.assertEqual(result.update_freq, "")
        self.assertEqual(result.counters, "")

    def test_transform_alias_response_multiple_types(self):
        """Test handling of different alias types"""
        type_test_cases = [
            ({"host": {"selected": 1}}, AliasType.HOST),
            ({"network": {"selected": 1}}, AliasType.NETWORK),
            ({"port": {"selected": 1}}, AliasType.PORT),
            ({"url": {"selected": 1}}, AliasType.URL),
            ({"geoip": {"selected": 1}}, AliasType.GEOIP),
        ]

        for type_dict, expected_type in type_test_cases:
            with self.subTest(type=expected_type):
                input_data = {"name": "test_alias", "type": type_dict}
                result = self.alias._transform_alias_response(self.test_uuid, input_data)
                self.assertEqual(result.type, expected_type)

    def test_transform_alias_response_content_variations(self):
        """Test different content variations"""
        test_cases = [
            # Empty content dictionary
            ({}, []),
            # Single content item
            ({"192.168.1.1": {"selected": 1, "value": "192.168.1.1"}}, ["192.168.1.1"]),
            # Multiple content items
            (
                {
                    "192.168.1.1": {"selected": 1, "value": "192.168.1.1"},
                    "192.168.1.2": {"selected": 1, "value": "192.168.1.2"},
                },
                ["192.168.1.1", "192.168.1.2"],
            ),
            # Mixed selected/unselected items
            (
                {
                    "192.168.1.1": {"selected": 1, "value": "192.168.1.1"},
                    "192.168.1.2": {"selected": 0, "value": "192.168.1.2"},
                },
                ["192.168.1.1"],
            ),
        ]

        for content_dict, expected_content in test_cases:
            with self.subTest(expected_content=expected_content):
                input_data = {"name": "test_alias", "type": {"host": {"selected": 1}}, "content": content_dict}
                result = self.alias._transform_alias_response(self.test_uuid, input_data)
                self.assertEqual(result.content, expected_content)

    def test_transform_alias_response_protocol_variations(self):
        """Test different protocol variations"""
        test_cases = [
            ({"IPv4": {"selected": 1}}, ProtocolType.IPV4),
            ({"IPv6": {"selected": 1}}, ProtocolType.IPV6),
            ({}, None),  # No protocol specified
        ]

        for proto_dict, expected_proto in test_cases:
            with self.subTest(protocol=expected_proto):
                input_data = {"name": "test_alias", "type": {"host": {"selected": 1}}, "proto": proto_dict}
                result = self.alias._transform_alias_response(self.test_uuid, input_data)
                self.assertEqual(result.proto, expected_proto)

    def test_transform_alias_response_validation_errors(self):
        """Test validation error cases"""
        # Missing required type field
        with self.assertRaises(ValidationError):
            input_data = {
                "name": "test_alias",
            }
            self.alias._transform_alias_response(self.test_uuid, input_data)

        # Invalid type
        with self.assertRaises(ValueError):
            input_data = {
                "name": "test_alias",
                "type": {"invalid_type": {"selected": 1}},
            }
            self.alias._transform_alias_response(self.test_uuid, input_data)

        # Invalid protocol
        with self.assertRaises(ValueError):
            input_data = {
                "name": "test_alias",
                "type": {"host": {"selected": 1}},
                "proto": {"invalid_proto": {"selected": 1}},
            }
            self.alias._transform_alias_response(self.test_uuid, input_data)

    def test_get_with_missing_name(self):
        """Test get method with missing required name field"""
        self.alias.fa.get_item = Mock(
            return_value={
                "alias": {
                    # Missing required 'name' field
                    "type": "host",
                }
            }
        )

        with self.assertRaises(ParsingError):
            self.alias.get("test-uuid")

    def test_get_with_missing_type(self):
        """Test get method with missing required type field"""
        self.alias.fa.get_item = Mock(
            return_value={
                "alias": {
                    "name": "test_alias",
                    # Missing required 'type' field
                }
            }
        )

        with self.assertRaises(ParsingError):
            self.alias.get("test-uuid")

    def test_get_with_invalid_type(self):
        """Test get method with invalid type in response"""
        self.alias.fa.get_item = Mock(
            return_value={
                "alias": {
                    "name": "test_alias",
                    "type": {"invalid_type": {"selected": 1}},
                }
            }
        )

        with self.assertRaises(ParsingError):
            self.alias.get("test-uuid")
