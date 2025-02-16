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
        rule_dict = rule.model_dump(exclude_unset=True)
        return self.ff.add_rule(body=rule_dict)

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
        rule_dict = rule.model_dump(exclude_unset=True)
        return self.ff.set_rule(uuid, body=rule_dict)

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
    def _transform_rule_response(rule_data: dict[str, Any]) -> dict[str, Any]:
        try:
            return {
                "sequence": int(rule_data.get("sequence", 0)),
                "action": rule_data.get("action"),
                "quick": bool(int(rule_data.get("quick", 1))),
                "interface": [iface.strip() for iface in rule_data.get("interface", "").split(",") if iface.strip()],
                "direction": rule_data.get("direction"),
                "ipprotocol": rule_data.get("ipprotocol"),
                "protocol": rule_data.get("protocol"),
                "source_net": rule_data.get("source_net"),
                "source_not": bool(int(rule_data.get("source_not", 0))),
                "source_port": rule_data.get("source_port"),
                "destination_net": rule_data.get("destination_net"),
                "destination_not": bool(int(rule_data.get("destination_not", 0))),
                "destination_port": rule_data.get("destination_port"),
                "gateway": rule_data.get("gateway"),
                "description": rule_data.get("description"),
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
