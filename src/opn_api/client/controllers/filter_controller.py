from typing import Any, Optional
from opn_api.api.core.firewall import FirewallFilter
from opn_api.models.firewall_models import (
    FirewallFilterRule,
    FirewallFilterRuleResponse,
)
from opn_api.exceptions import ParsingError


class FilterController:
    def __init__(self, client):
        self.ff = FirewallFilter(client)

    def add_rule(self, rule: FirewallFilterRule) -> dict[str, Any]:
        request_body = self._prepare_rule_body(rule)
        return self.ff.add_rule(body=request_body)

    def delete_rule(self, uuid: str) -> dict[str, Any]:
        return self.ff.del_rule(uuid)

    def get_rule(self, uuid: str) -> FirewallFilterRuleResponse:
        response = self.ff.get_rule(uuid)
        rule_data = response.get("rule")
        if rule_data:
            try:
                model_data = self._transform_rule_response(rule_data)
                return FirewallFilterRuleResponse(uuid=uuid, **model_data)
            except Exception as error:
                raise ParsingError(f"Failed to parse the rule with UUID: {uuid}", rule_data, str(error)) from error
        raise ValueError(f"No rule found with UUID: {uuid}")

    def set_rule(self, uuid: str, rule: FirewallFilterRule) -> dict[str, Any]:
        request_body = self._prepare_rule_body(rule)
        return self.ff.set_rule(uuid, body=request_body)

    def toggle_rule(self, uuid: str, enabled: Optional[bool] = None) -> dict[str, Any]:
        if enabled is None:
            current_rule = self.get_rule(uuid)
            enabled = not current_rule.enabled
        return self.ff.toggle_rule(uuid, body={"enabled": int(enabled)})

    def apply_changes(self) -> dict[str, Any]:
        return self.ff.apply()

    def create_savepoint(self) -> dict[str, Any]:
        return self.ff.savepoint()

    def cancel_rollback(self) -> dict[str, Any]:
        return self.ff.cancel_rollback()

    def list_rules(self) -> list[FirewallFilterRuleResponse]:
        response = self.ff.search_rule(body={})
        rows = response.get("rows", [])
        rules = []
        for rule_data in rows:
            try:
                rule = self._parse_rule_search_item(rule_data)
                rules.append(rule)
            except Exception as error:
                raise ParsingError("Failed to parse rule in list", rule_data, str(error)) from error
        return rules

    def match_rule_by_attributes(self, **attributes) -> list[dict[str, Any]]:
        all_rules = self.list_rules()
        matched_rules = [
            rule.model_dump()
            for rule in all_rules
            if all(rule.model_dump().get(key) == value for key, value in attributes.items())
        ]
        return matched_rules

    @staticmethod
    def _prepare_rule_body(rule: FirewallFilterRule) -> dict[str, Any]:
        """
        Prepares the firewall filter rule body for API submission.

        Transforms the Pydantic model into the format expected by the OPNsense API:
        - Wraps data in {"rule": {...}}
        - Converts booleans to "1" or "0" strings
        - Converts interface list to comma-separated string
        - Converts enums to their string values
        - Converts None to empty strings
        """
        # Convert interface list to comma-separated string
        interface_str = ",".join(rule.interface) if rule.interface else ""

        return {
            "rule": {
                "sequence": str(rule.sequence),
                "action": rule.action.value,
                "quick": str(int(rule.quick)),
                "interface": interface_str,
                "direction": rule.direction.value,
                "ipprotocol": rule.ipprotocol.value,
                "protocol": rule.protocol.value,
                "source_net": rule.source_net or "",
                "source_not": str(int(rule.source_not)),
                "source_port": rule.source_port or "",
                "destination_net": rule.destination_net or "",
                "destination_not": str(int(rule.destination_not)),
                "destination_port": rule.destination_port or "",
                "gateway": rule.gateway or "",
                "description": rule.description or "",
                "enabled": str(int(rule.enabled)),
                "log": str(int(rule.log)),
            }
        }

    @staticmethod
    def _transform_rule_response(rule_data: dict[str, Any]) -> dict[str, Any]:
        """
        Transforms rule data from get_rule endpoint to FirewallFilterRuleResponse format.

        The get_rule endpoint returns structured data with dictionaries for select fields.
        For example:
            "action": {"block": {"selected": 1, "value": "Block"}, "pass": {...}}
        We need to extract the selected value from these dicts.
        """
        try:
            # Helper function to extract selected value from dict fields
            def extract_selected_value(field_data):
                if isinstance(field_data, dict):
                    # Find the selected item
                    for key, value in field_data.items():
                        if isinstance(value, dict) and value.get("selected") == 1:
                            return key
                    # If nothing selected, return first key
                    return next(iter(field_data.keys())) if field_data else ""
                return field_data or ""

            # Extract interface - can be dict or string
            interface_data = rule_data.get("interface", "")
            if isinstance(interface_data, dict):
                # Extract selected interfaces from dict
                interfaces = [key for key, value in interface_data.items()
                             if isinstance(value, dict) and value.get("selected") == 1]
            else:
                # Handle comma-separated string
                interfaces = [iface.strip() for iface in str(interface_data).split(",") if iface.strip()]

            return {
                "sequence": int(rule_data.get("sequence", 0)),
                "action": extract_selected_value(rule_data.get("action")),
                "quick": bool(int(rule_data.get("quick", 1))),
                "interface": interfaces,
                "direction": extract_selected_value(rule_data.get("direction")),
                "ipprotocol": extract_selected_value(rule_data.get("ipprotocol")),
                "protocol": extract_selected_value(rule_data.get("protocol")),
                "source_net": rule_data.get("source_net", ""),
                "source_not": bool(int(rule_data.get("source_not", 0))),
                "source_port": rule_data.get("source_port", ""),
                "destination_net": rule_data.get("destination_net", ""),
                "destination_not": bool(int(rule_data.get("destination_not", 0))),
                "destination_port": rule_data.get("destination_port", ""),
                "gateway": extract_selected_value(rule_data.get("gateway")) if isinstance(rule_data.get("gateway"), dict) else rule_data.get("gateway", ""),
                "description": rule_data.get("description", ""),
                "enabled": bool(int(rule_data.get("enabled", 1))),
                "log": bool(int(rule_data.get("log", 0))),
            }
        except (TypeError, ValueError) as error:
            raise ParsingError("Invalid rule data structure", rule_data, str(error)) from error

    @staticmethod
    def _parse_rule_search_item(rule_data: dict[str, Any]) -> FirewallFilterRuleResponse:
        try:
            return FirewallFilterRuleResponse(
                uuid=rule_data.get("uuid", ""),
                sequence=int(rule_data.get("sequence", 0)),
                action=rule_data.get("action"),
                quick=bool(int(rule_data.get("quick", 1))),
                interface=[iface.strip() for iface in rule_data.get("interface", "").split(",") if iface.strip()],
                direction=rule_data.get("direction"),
                ipprotocol=rule_data.get("ipprotocol"),
                protocol=rule_data.get("protocol"),
                source_net=rule_data.get("source_net"),
                source_not=bool(int(rule_data.get("source_not", 0))),
                source_port=rule_data.get("source_port"),
                destination_net=rule_data.get("destination_net"),
                destination_not=bool(int(rule_data.get("destination_not", 0))),
                destination_port=rule_data.get("destination_port"),
                gateway=rule_data.get("gateway"),
                description=rule_data.get("description"),
                enabled=bool(int(rule_data.get("enabled", 1))),
                log=bool(int(rule_data.get("log", 0))),
            )
        except (TypeError, ValueError) as error:
            raise ParsingError("Invalid rule data structure in search item", rule_data, str(error)) from error
