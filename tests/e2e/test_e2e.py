import os
import pytest
from dotenv import load_dotenv
from opn_api.api.client import OPNsenseClientConfig, OPNAPIClient
from opn_api.client import OPNFirewallClient


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
        timeout=10,
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
    dhcp_client = OPNFirewallClient(opn_api_client)
    response = dhcp_client.dhcp.list_leases()
    for lease in response.rows:
        print(lease)


@pytest.mark.skipif(skip_e2e, reason=skip_reason)
def test_alias_list_all(opn_api_client):
    """
    Tests listing all firewall aliases including system-generated aliases.

    This test validates PR #4 fix for parsing system aliases:
    - OPNsense < 25.7: Returns "external (advanced)", "internal (automatic)"
    - OPNsense >= 25.7: Returns "external", "internal"

    The library should handle both formats without raising Pydantic validation errors.
    """
    print("\nTesting Firewall Alias List (validates system alias parsing)...")
    fw_client = OPNFirewallClient(opn_api_client)

    # This should not raise any validation errors
    aliases = fw_client.alias.list()

    assert isinstance(aliases, list), "Expected list() to return a list"
    assert len(aliases) > 0, "Expected at least one alias to exist"

    # Find system-generated aliases
    system_aliases = {
        "external": [],  # bogons, bogonsv6, sshlockout, virusprot
        "internal": []   # __lan_network, __wan_network, etc.
    }

    user_aliases = []

    for alias in aliases:
        # Print each alias for inspection
        print(f"  - {alias.name}: type={alias.type.value}, proto={alias.proto}, enabled={alias.enabled}")

        # Categorize aliases
        if alias.type.value in ["external", "external (advanced)"]:
            system_aliases["external"].append(alias)
        elif alias.type.value in ["internal", "internal (automatic)"]:
            system_aliases["internal"].append(alias)
        else:
            user_aliases.append(alias)

    # Validation checks
    print(f"\nFound {len(system_aliases['external'])} external system aliases")
    print(f"Found {len(system_aliases['internal'])} internal system aliases")
    print(f"Found {len(user_aliases)} user-defined aliases")

    # Most OPNsense installations should have these system aliases
    common_external_aliases = ["bogons", "bogonsv6", "sshlockout", "virusprot"]
    common_internal_aliases = ["__lan_network", "__wan_network"]

    external_names = [a.name for a in system_aliases["external"]]
    internal_names = [a.name for a in system_aliases["internal"]]

    print(f"\nExternal system aliases found: {external_names}")
    print(f"Internal system aliases found: {internal_names}")

    # Check if common system aliases are present (not all systems may have all of them)
    if system_aliases["external"]:
        print("✓ Successfully parsed external system aliases")
    if system_aliases["internal"]:
        print("✓ Successfully parsed internal system aliases")


@pytest.mark.skipif(skip_e2e, reason=skip_reason)
def test_alias_with_empty_proto(opn_api_client):
    """
    Tests that aliases with empty proto field are handled correctly.

    This validates the field_validator fix in PR #4 that converts empty
    string proto values to None for alias types like port, url, mac, etc.
    """
    print("\nTesting Firewall Alias with empty proto field...")
    fw_client = OPNFirewallClient(opn_api_client)

    aliases = fw_client.alias.list()

    # Find aliases with None proto (which should have been empty strings from API)
    aliases_without_proto = [a for a in aliases if a.proto is None]

    assert len(aliases_without_proto) > 0, "Expected at least one alias with empty proto field"

    print(f"Found {len(aliases_without_proto)} aliases with proto=None (converted from empty string)")

    for alias in aliases_without_proto[:5]:  # Print first 5 examples
        print(f"  - {alias.name}: type={alias.type.value}, proto={alias.proto}")

    print("✓ Successfully handled empty proto fields")


@pytest.mark.skipif(skip_e2e, reason=skip_reason)
def test_alias_get_system_alias(opn_api_client):
    """
    Tests fetching a specific system alias by UUID using get() method.

    This ensures that the get_item endpoint also correctly handles
    system alias types in both old and new formats.
    """
    print("\nTesting Firewall Alias get() for system aliases...")
    fw_client = OPNFirewallClient(opn_api_client)

    # First, get the list to find a system alias UUID
    aliases = fw_client.alias.list()

    # Find a system alias (prefer bogons as it's common)
    system_alias = None
    for alias in aliases:
        if alias.name == "bogons":
            system_alias = alias
            break

    # Fallback to any external or internal alias
    if not system_alias:
        for alias in aliases:
            if alias.type.value in ["external", "external (advanced)", "internal", "internal (automatic)"]:
                system_alias = alias
                break

    if system_alias:
        print(f"Testing get() for system alias: {system_alias.name} (UUID: {system_alias.uuid})")

        # This should not raise any validation errors
        fetched_alias = fw_client.alias.get(system_alias.uuid)

        assert fetched_alias.uuid == system_alias.uuid
        assert fetched_alias.name == system_alias.name
        print(f"  - Successfully fetched: {fetched_alias.name}, type={fetched_alias.type.value}")
        print("✓ System alias get() works correctly")
    else:
        print("⚠ No system aliases found to test get() method")


@pytest.mark.skipif(skip_e2e, reason=skip_reason)
def test_alias_parsing_consistency(opn_api_client):
    """
    Tests that the same alias returns consistent data from list() and get() methods.

    This validates that both API endpoints (search_item and get_item) are
    handled correctly by the parsing logic.
    """
    print("\nTesting Firewall Alias parsing consistency between list() and get()...")
    fw_client = OPNFirewallClient(opn_api_client)

    # Get all aliases
    aliases = fw_client.alias.list()

    if len(aliases) == 0:
        pytest.skip("No aliases found to test consistency")

    # Test first 3 aliases for consistency
    test_count = min(3, len(aliases))

    for alias in aliases[:test_count]:
        print(f"\nTesting consistency for alias: {alias.name}")

        # Fetch the same alias using get()
        fetched_alias = fw_client.alias.get(alias.uuid)

        # Compare critical fields
        assert fetched_alias.uuid == alias.uuid, f"UUID mismatch for {alias.name}"
        assert fetched_alias.name == alias.name, f"Name mismatch for {alias.name}"
        assert fetched_alias.enabled == alias.enabled, f"Enabled mismatch for {alias.name}"

        # Type should match (accounting for both old and new formats)
        assert fetched_alias.type.value == alias.type.value, f"Type mismatch for {alias.name}"

        print(f"  ✓ Consistency validated for {alias.name}")

    print(f"\n✓ All {test_count} aliases show consistent data between list() and get()")

