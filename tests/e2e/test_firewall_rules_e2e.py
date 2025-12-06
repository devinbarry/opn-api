import os
import pytest
from dotenv import load_dotenv
from opn_api.api.client import OPNsenseClientConfig, OPNAPIClient
from opn_api.client import OPNFirewallClient
from opn_api.models.firewall_models import (
    FirewallFilterRule,
    Action,
    Direction,
    IPProtocol,
    Protocol,
)


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
def test_list_firewall_rules(opn_api_client):
    """
    Tests listing all firewall filter rules.

    This validates that the FilterController can successfully fetch and parse
    rules from a real OPNsense instance.
    """
    print("\nTesting Firewall Filter Rule List...")
    fw_client = OPNFirewallClient(opn_api_client)

    # Fetch all rules
    rules = fw_client.filter.list_rules()

    assert isinstance(rules, list), "Expected list_rules() to return a list"
    print(f"Found {len(rules)} firewall rules")

    # If there are rules, validate their structure
    if len(rules) > 0:
        first_rule = rules[0]
        print(f"\nExample rule:")
        print(f"  - UUID: {first_rule.uuid}")
        print(f"  - Description: {first_rule.description}")
        print(f"  - Action: {first_rule.action.value}")
        print(f"  - Direction: {first_rule.direction.value}")
        print(f"  - Protocol: {first_rule.protocol.value}")
        print(f"  - Interface: {first_rule.interface}")
        print(f"  - Source: {first_rule.source_net}")
        print(f"  - Destination: {first_rule.destination_net}")
        print(f"  - Enabled: {first_rule.enabled}")

        # Validate fields are properly parsed
        assert hasattr(first_rule, 'uuid')
        assert hasattr(first_rule, 'action')
        assert hasattr(first_rule, 'direction')
        assert hasattr(first_rule, 'protocol')
        assert isinstance(first_rule.interface, list), "Interface should be a list"
        assert isinstance(first_rule.enabled, bool), "Enabled should be a boolean"
        assert isinstance(first_rule.quick, bool), "Quick should be a boolean"

        print("\n✓ Successfully listed and parsed firewall rules")
    else:
        print("⚠ No firewall rules found on this OPNsense instance")


@pytest.mark.skipif(skip_e2e, reason=skip_reason)
def test_get_specific_firewall_rule(opn_api_client):
    """
    Tests fetching a specific firewall rule by UUID.

    This validates that get_rule() properly parses individual rule data
    from the OPNsense API.
    """
    print("\nTesting Firewall Filter Rule get()...")
    fw_client = OPNFirewallClient(opn_api_client)

    # First, get the list to find a rule UUID
    rules = fw_client.filter.list_rules()

    if len(rules) == 0:
        pytest.skip("No firewall rules found to test get() method")

    # Test get() on the first rule
    test_rule = rules[0]
    print(f"Testing get() for rule: {test_rule.description or test_rule.uuid}")

    # Fetch the same rule using get()
    fetched_rule = fw_client.filter.get_rule(test_rule.uuid)

    # Validate the fetched rule matches
    assert fetched_rule.uuid == test_rule.uuid
    assert fetched_rule.action == test_rule.action
    assert fetched_rule.direction == test_rule.direction
    assert fetched_rule.protocol == test_rule.protocol
    assert fetched_rule.enabled == test_rule.enabled

    print(f"  ✓ Successfully fetched rule: {fetched_rule.description or fetched_rule.uuid}")
    print("✓ get_rule() works correctly")


@pytest.mark.skipif(skip_e2e, reason=skip_reason)
def test_add_and_delete_firewall_rule(opn_api_client):
    """
    Tests adding and deleting a firewall rule.

    This is the critical test that validates the fix for issue #1.
    It ensures that _prepare_rule_body() correctly formats the request
    data for the OPNsense API.

    IMPORTANT: This test will:
    1. Add a test rule (disabled for safety)
    2. Verify it was created correctly
    3. Delete the test rule
    4. NOT apply changes (so firewall is not affected)
    """
    print("\nTesting Firewall Filter Rule add() and delete()...")
    fw_client = OPNFirewallClient(opn_api_client)

    # Create a test rule (DISABLED for safety)
    test_rule = FirewallFilterRule(
        sequence=99999,
        action=Action.BLOCK,
        quick=True,
        interface=["lan"],
        direction=Direction.IN,
        ipprotocol=IPProtocol.INET,
        protocol=Protocol.TCP,
        source_net="192.0.2.0/24",  # TEST-NET-1 (RFC 5737) - safe test range
        source_not=False,
        destination_net="198.51.100.0/24",  # TEST-NET-2 (RFC 5737) - safe test range
        destination_not=False,
        destination_port="12345",
        description="E2E Test Rule - Safe to Delete",
        enabled=False,  # DISABLED for safety
        log=False,
    )

    print("Creating test rule (disabled, will not affect firewall)...")

    # Add the rule - this is where issue #1 would have failed
    add_response = fw_client.filter.add_rule(test_rule)

    print(f"  Add response: {add_response}")
    assert "result" in add_response, "Expected 'result' in add_rule response"

    if add_response.get("result") == "saved":
        print("  ✓ Rule added successfully")

        # Get the UUID from the response
        rule_uuid = add_response.get("uuid")
        assert rule_uuid, "Expected UUID in add_rule response"
        print(f"  New rule UUID: {rule_uuid}")

        # Verify the rule was created by fetching it
        print("  Verifying rule was created...")
        created_rule = fw_client.filter.get_rule(rule_uuid)

        assert created_rule.uuid == rule_uuid
        assert created_rule.description == "E2E Test Rule - Safe to Delete"
        assert created_rule.action == Action.BLOCK
        assert created_rule.enabled == False, "Test rule should be disabled"
        assert "lan" in created_rule.interface
        print("  ✓ Rule verified in OPNsense")

        # Delete the test rule
        print("  Cleaning up: Deleting test rule...")
        delete_response = fw_client.filter.delete_rule(rule_uuid)
        print(f"  Delete response: {delete_response}")

        assert "result" in delete_response, "Expected 'result' in delete_rule response"
        print("  ✓ Test rule deleted")

        print("\n✓ Add and delete operations work correctly")
        print("✓ Issue #1 fix validated: _prepare_rule_body() formats data correctly!")

        # Note: We do NOT call apply_changes() to avoid affecting the actual firewall
        print("\nNote: Changes were NOT applied - firewall configuration unchanged")
    else:
        pytest.fail(f"Failed to add test rule. Response: {add_response}")


@pytest.mark.skipif(skip_e2e, reason=skip_reason)
def test_update_firewall_rule(opn_api_client):
    """
    Tests updating a firewall rule.

    This validates that set_rule() properly formats the request body.

    Creates a test rule, updates it, then deletes it.
    Does NOT apply changes to avoid affecting the firewall.
    """
    print("\nTesting Firewall Filter Rule set_rule()...")
    fw_client = OPNFirewallClient(opn_api_client)

    # Create a test rule first
    test_rule = FirewallFilterRule(
        sequence=99998,
        action=Action.PASS,
        quick=True,
        interface=["lan"],
        direction=Direction.OUT,
        ipprotocol=IPProtocol.INET,
        protocol=Protocol.UDP,
        source_net="192.0.2.0/24",
        destination_net="198.51.100.0/24",
        description="E2E Test Rule for Update - Safe to Delete",
        enabled=False,
        log=False,
    )

    print("Creating test rule for update test...")
    add_response = fw_client.filter.add_rule(test_rule)

    if add_response.get("result") != "saved":
        pytest.skip(f"Could not create test rule for update test: {add_response}")

    rule_uuid = add_response.get("uuid")
    print(f"  Created rule UUID: {rule_uuid}")

    try:
        # Update the rule
        updated_rule = FirewallFilterRule(
            sequence=99997,  # Changed
            action=Action.BLOCK,  # Changed
            quick=False,  # Changed
            interface=["lan", "wan"],  # Changed - multiple interfaces
            direction=Direction.IN,  # Changed
            ipprotocol=IPProtocol.INET6,  # Changed
            protocol=Protocol.TCP,  # Changed
            source_net="2001:db8::/32",  # Changed to IPv6
            destination_net="2001:db8:1::/48",  # Changed to IPv6
            destination_port="443",  # Added
            description="E2E Test Rule UPDATED - Safe to Delete",  # Changed
            enabled=False,  # Still disabled
            log=True,  # Changed
        )

        print("  Updating rule...")
        update_response = fw_client.filter.set_rule(rule_uuid, updated_rule)
        print(f"  Update response: {update_response}")

        assert "result" in update_response, "Expected 'result' in set_rule response"

        if update_response.get("result") == "saved":
            print("  ✓ Rule updated successfully")

            # Verify the update
            print("  Verifying update...")
            fetched_rule = fw_client.filter.get_rule(rule_uuid)

            assert fetched_rule.uuid == rule_uuid
            assert fetched_rule.description == "E2E Test Rule UPDATED - Safe to Delete"
            assert fetched_rule.action == Action.BLOCK
            assert fetched_rule.direction == Direction.IN
            assert fetched_rule.ipprotocol == IPProtocol.INET6
            assert fetched_rule.protocol == Protocol.TCP
            assert set(fetched_rule.interface) == {"lan", "wan"}, "Should have both interfaces"
            assert fetched_rule.log == True
            print("  ✓ Update verified")

            print("\n✓ set_rule() works correctly")
        else:
            pytest.fail(f"Failed to update rule. Response: {update_response}")

    finally:
        # Clean up: Delete the test rule
        print("  Cleaning up: Deleting test rule...")
        delete_response = fw_client.filter.delete_rule(rule_uuid)
        print(f"  Delete response: {delete_response}")
        print("  ✓ Test rule deleted")

        print("\nNote: Changes were NOT applied - firewall configuration unchanged")


@pytest.mark.skipif(skip_e2e, reason=skip_reason)
def test_rule_body_formatting_validation(opn_api_client):
    """
    Tests that _prepare_rule_body correctly formats all field types.

    This test validates the specific transformations that fix issue #1:
    - Booleans → "0"/"1" strings
    - Interface list → comma-separated string
    - Enums → string values
    - None → empty strings
    """
    print("\nTesting _prepare_rule_body() formatting...")
    fw_client = OPNFirewallClient(opn_api_client)

    # Create a rule with diverse field types
    test_rule = FirewallFilterRule(
        sequence=1,
        action=Action.REJECT,  # Enum
        quick=False,  # Boolean False
        interface=["opt1", "opt2", "opt3"],  # Multiple interfaces
        direction=Direction.OUT,  # Enum
        ipprotocol=IPProtocol.INET6,  # Enum
        protocol=Protocol.ICMP,  # Enum
        source_net="any",
        source_not=True,  # Boolean True
        source_port=None,  # None value
        destination_net="any",
        destination_not=False,  # Boolean False
        destination_port=None,  # None value
        gateway=None,  # None value
        description="Format validation test",
        enabled=True,  # Boolean True
        log=True,  # Boolean True
    )

    # Call _prepare_rule_body directly
    prepared_body = fw_client.filter._prepare_rule_body(test_rule)

    print("Validating prepared body structure...")

    # Verify structure
    assert "rule" in prepared_body, "Body should be wrapped in 'rule' key"
    rule_data = prepared_body["rule"]

    # Verify type conversions
    print("  Checking type conversions:")

    # Booleans → strings
    assert rule_data["quick"] == "0", f"Boolean False should be '0', got {rule_data['quick']}"
    print("    ✓ Boolean False → '0'")

    assert rule_data["source_not"] == "1", f"Boolean True should be '1', got {rule_data['source_not']}"
    print("    ✓ Boolean True → '1'")

    assert rule_data["enabled"] == "1", f"enabled=True should be '1', got {rule_data['enabled']}"
    print("    ✓ enabled=True → '1'")

    assert rule_data["log"] == "1", f"log=True should be '1', got {rule_data['log']}"
    print("    ✓ log=True → '1'")

    # List → comma-separated string
    assert rule_data["interface"] == "opt1,opt2,opt3", f"List should be comma-separated, got {rule_data['interface']}"
    print("    ✓ interface list → 'opt1,opt2,opt3'")

    # Enums → string values
    assert rule_data["action"] == "reject", f"Enum should be value, got {rule_data['action']}"
    print("    ✓ Action enum → 'reject'")

    assert rule_data["direction"] == "out", f"Enum should be value, got {rule_data['direction']}"
    print("    ✓ Direction enum → 'out'")

    assert rule_data["ipprotocol"] == "inet6", f"Enum should be value, got {rule_data['ipprotocol']}"
    print("    ✓ IPProtocol enum → 'inet6'")

    # None → empty strings
    assert rule_data["source_port"] == "", f"None should be empty string, got {rule_data['source_port']}"
    print("    ✓ None → '' (source_port)")

    assert rule_data["destination_port"] == "", f"None should be empty string, got {rule_data['destination_port']}"
    print("    ✓ None → '' (destination_port)")

    assert rule_data["gateway"] == "", f"None should be empty string, got {rule_data['gateway']}"
    print("    ✓ None → '' (gateway)")

    # Integers → strings
    assert rule_data["sequence"] == "1", f"Int should be string, got {rule_data['sequence']}"
    print("    ✓ sequence int → '1'")

    print("\n✓ All field type conversions are correct")
    print("✓ _prepare_rule_body() formats data exactly as OPNsense API expects")
