import json
from unittest import TestCase
from unittest.mock import patch
from opn_api.api.client import OPNAPIClient, OPNsenseClientConfig
from opn_api.exceptions import APIException


class TestApiClient(TestCase):
    def create_client_config(self, api_key, api_secret, base_url, ssl_verify_cert, ca, timeout):
        return OPNsenseClientConfig(
            api_key=api_key,
            api_secret=api_secret,
            base_url=base_url,
            ssl_verify_cert=ssl_verify_cert,
            ca=ca,
            timeout=timeout,
        )

    @patch("opn_api.api.client.requests.get")
    def test_execute_get_success(self, request_mock):
        api_response_fixture = {"product_id": "opnsense"}
        request_mock.return_value.status_code = 200
        request_mock.return_value.headers = {"content-type": "application/json; charset=UTF-8"}
        request_mock.return_value.text = json.dumps(api_response_fixture)

        config = self.create_client_config(
            "api_key", "api_secret", "https://127.0.0.1/api", True, "~/.opn-cli/ca.pem", 60
        )
        api_config = {
            "module": "Core",
            "controller": "firmware",
            "method": "get",
            "command": "info",
        }
        api_parameters = []

        client = OPNAPIClient(config)
        result = client.execute(*api_parameters, **api_config)

        request_mock.assert_called_once_with(
            "https://127.0.0.1/api/core/firmware/info",
            verify="~/.opn-cli/ca.pem",
            auth=("api_key", "api_secret"),
            timeout=60,
        )
        self.assertEqual(api_response_fixture, result)

    @patch("opn_api.api.client.requests.get")
    def test_execute_content_types(self, request_mock):
        api_response_fixture = """
        <?xml version="1.0"?>
        <opnsense>
        </opnsense>
        """
        request_mock.return_value.status_code = 200
        request_mock.return_value.headers = {"content-type": "application/octet-stream"}
        request_mock.return_value.text = api_response_fixture

        config = self.create_client_config(
            "api_key", "api_secret", "https://127.0.0.1/api", True, "~/.opn-cli/ca.pem", 60
        )
        api_config = {
            "module": "Core",
            "controller": "backup",
            "method": "get",
            "command": "download",
        }
        api_parameters = []

        client = OPNAPIClient(config)
        result = client.execute(*api_parameters, **api_config)

        request_mock.assert_called_once_with(
            "https://127.0.0.1/api/core/backup/download",
            verify="~/.opn-cli/ca.pem",
            auth=("api_key", "api_secret"),
            timeout=60,
        )
        self.assertEqual(api_response_fixture, result)

    @patch("opn_api.api.client.requests.get")
    def test_execute_get_failure(self, request_mock):
        request_mock.return_value.status_code = 400
        request_mock.return_value.text = {
            "message": "controller OPNsense\\Core\\Api\\IndexController not found",
            "status": 400,
        }
        request_mock.return_value.url = "https://127.0.0.1/api/not/existing/confusion"

        config = self.create_client_config(
            "api_key", "api_secret", "https://127.0.0.1/api", True, "~/.opn-cli/ca.pem", 60
        )
        api_config = {
            "module": "Not",
            "controller": "Existing",
            "method": "get",
            "command": "confusion",
        }
        api_parameters = []

        client = OPNAPIClient(config)
        self.assertRaises(APIException, client.execute, *api_parameters, **api_config)
        request_mock.assert_called_once_with(
            "https://127.0.0.1/api/not/existing/confusion",
            verify="~/.opn-cli/ca.pem",
            auth=("api_key", "api_secret"),
            timeout=60,
        )

    @patch("opn_api.api.client.requests.post")
    def test_execute_post_json_success(self, request_mock):
        api_response_fixture = [{"status": "ok", "msg_uuid": "8a0a415a-dbee-410d-be9f-01b90d71ff7c"}]
        request_mock.return_value.headers = {"content-type": "application/json; charset=UTF-8"}
        request_mock.return_value.status_code = 200
        request_mock.return_value.text = json.dumps(api_response_fixture)

        config = self.create_client_config(
            "api_key2", "api_secret2", "https://127.0.0.1/api", False, "~/.opn-cli/ca.pem", 40
        )
        api_config = {
            "module": "openvpn",
            "controller": "export",
            "method": "post",
            "command": "download",
        }
        api_parameters = ["vpnid", "certref"]

        api_payload = {
            "param1": 0,
            "param2": "test",
            "paramN": "testN",
        }

        client = OPNAPIClient(config)
        result = client.execute(*api_parameters, body=api_payload, **api_config)

        request_mock.assert_called_once_with(
            "https://127.0.0.1/api/openvpn/export/download/vpnid/certref",
            json=api_payload,
            verify=False,
            auth=("api_key2", "api_secret2"),
            timeout=40,
        )
        self.assertEqual(api_response_fixture, result)

    def test_execute_failure(self):
        config = self.create_client_config(
            "api_key3", "api_secret3", "https://127.0.0.1/api", False, "~/.opn-cli/ca.pem", 10
        )
        api_config = {
            "module": "Core",
            "controller": "Firmware",
            "method": "head",
            "command": "reinstall",
        }
        api_parameters = []

        client = OPNAPIClient(config)
        self.assertRaises(APIException, client.execute, *api_parameters, **api_config)
