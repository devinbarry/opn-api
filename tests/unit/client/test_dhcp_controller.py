import unittest
from unittest.mock import Mock

from opn_api.client.controllers.dhcp_controller import DhcpLeaseController
from opn_api.models.dhcp import DhcpLeaseResponse, DhcpLeaseType, DhcpLeaseStatus
from opn_api.exceptions import ParsingError


class TestDhcpLeaseController(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.controller = DhcpLeaseController(self.mock_client)
        # Replace API interfaces with mocks
        self.controller.dhcp_api = Mock()
        self.controller.service_api = Mock()

    def test_list_leases_success(self):
        # Prepare stub response data
        row_data = {
            "address": "192.0.2.1",
            "starts": "",
            "ends": "",
            "cltt": None,
            "binding": None,
            "uid": None,
            "client-hostname": None,
            "type": "dynamic",
            "status": "online",
            "descr": "",
            "mac": "00:11:22:33:44:55",
            "hostname": "host1",
            "state": "active",
            "man": "",  # Manufacturer
            "if": "em0",
            "if_descr": "WAN",
        }
        stub_data = {
            "total": 1,
            "rowCount": 1,
            "current": 1,
            "rows": [row_data],
            "interfaces": {"em0": "WAN"},
        }
        self.controller.dhcp_api.search_lease.return_value = stub_data

        response = self.controller.list_leases()
        # Verify response model
        self.assertIsInstance(response, DhcpLeaseResponse)
        self.assertEqual(response.total, 1)
        self.assertEqual(response.row_count, 1)
        self.assertEqual(response.current, 1)
        self.assertEqual(response.interfaces, {"em0": "WAN"})
        # Verify single lease entry
        self.assertEqual(len(response.rows), 1)
        lease = response.rows[0]
        self.assertEqual(str(lease.address), "192.0.2.1")
        self.assertIsNone(lease.starts)
        self.assertIsNone(lease.ends)
        self.assertEqual(lease.interface, "em0")
        self.assertEqual(lease.interface_description, "WAN")
        self.assertEqual(lease.type, DhcpLeaseType.DYNAMIC)
        self.assertEqual(lease.status, DhcpLeaseStatus.ONLINE)

    def test_list_leases_parsing_error(self):
        # Simulate invalid API response causing validation to fail
        bad_data = {"invalid": True}
        self.controller.dhcp_api.search_lease.return_value = bad_data
        with self.assertRaises(ParsingError) as cm:
            self.controller.list_leases()
        err = cm.exception
        self.assertEqual(err.message, "Failed to parse DHCP lease list response")
        self.assertEqual(err.data, bad_data)
        # Details should mention missing required fields
        self.assertIn("Field required", err.details)

    def test_delete_lease(self):
        # Ensure the delete_lease method proxies to the API
        self.controller.dhcp_api.del_lease.return_value = {"result": "deleted"}
        result = self.controller.delete_lease("192.0.2.1")
        self.controller.dhcp_api.del_lease.assert_called_once_with("192.0.2.1")
        self.assertEqual(result, {"result": "deleted"})

    def test_apply_changes(self):
        # Ensure apply_changes calls service_api.reconfigure
        self.controller.service_api.reconfigure.return_value = {"result": "ok"}
        result = self.controller.apply_changes()
        self.controller.service_api.reconfigure.assert_called_once()
        self.assertEqual(result, {"result": "ok"})