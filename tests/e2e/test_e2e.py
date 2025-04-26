import os
import pytest
from dotenv import load_dotenv
from opn_api.api.client import OPNsenseClientConfig, OPNAPIClient
from opn_api.api.core.dhcp_v4 import Leases as DhcpV4Leases

# Load environment variables from .env file
load_dotenv()

# Check if required environment variables are set
API_KEY = os.getenv("OPNSENSE_API_KEY")
API_SECRET = os.getenv("OPNSENSE_API_SECRET")
BASE_URL = os.getenv("OPNSENSE_BASE_URL")
SSL_VERIFY = os.getenv("OPNSENSE_SSL_VERIFY", "true").lower() == "true"

# Skip E2E tests if connection details are not provided
skip_e2e = not all([API_KEY, API_SECRET, BASE_URL])
skip_reason = "Skipping E2E tests: OPNsense connection details not found in environment variables."


@pytest.fixture(scope="module")
def opn_api_client():
    """Fixture to create and provide the OPNAPIClient instance."""
    if skip_e2e:
        pytest.skip(skip_reason)

    config = OPNsenseClientConfig(
        api_key=API_KEY,
        api_secret=API_SECRET,
        base_url=BASE_URL,
        ssl_verify_cert=SSL_VERIFY,
        timeout=10, # Reduced timeout for tests
    )
    client = OPNAPIClient(config)
    return client


@pytest.mark.skipif(skip_e2e, reason=skip_reason)
def test_dhcp_v4_search_lease(opn_api_client):
    """
    Tests fetching leases using the DHCPv4 Leases controller.
    Prints the raw response for inspection.
    """
    print("\nTesting DHCPv4 Leases Controller (module: dhcpv4, controller: leases)...")
    dhcp_v4_leases_api = DhcpV4Leases(opn_api_client)
    try:
        response = dhcp_v4_leases_api.search_lease()
        print("Response from dhcpv4/leases/searchLease:")
        print(response)
        assert isinstance(response, dict) # Basic check that we got a dict back
    except Exception as e:
        pytest.fail(f"API call failed: {e}")
