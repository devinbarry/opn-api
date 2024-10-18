from typing import Any
from opn_api.api.core.firewall import FirewallFilter
from opn_api.models.firewall_models import FirewallFilterRule, FirewallFilterRuleResponse
from opn_api.exceptions import ParsingError


class FilterController:
    def __init__(self, client):
        self.ff = FirewallFilter(client)

    def add_rule(self, rule: FirewallFilterRule) -> dict:
        rule_dict = rule.dict(exclude_unset=True)
        return self.ff.add_rule(json=rule_dict)

    def delete_rule(self, uuid: str) -> dict:
        return self.ff.del_rule(uuid)

    def get_rule(self, uuid: str = None) -> FirewallFilterRuleResponse:
        response = self.ff.get_rule(uuid)
        if 'rule' in response:
            try:
                rule_data = response['rule']
                model_data = self._transform_rule_response(rule_data)
                return FirewallFilterRuleResponse(uuid=uuid, **model_data)
            except Exception as error:
                raise ParsingError(f"Failed to parse the rule with UUID: {uuid}", rule_data, str(error))
        raise ValueError(f"No rule found with UUID: {uuid}")

    def set_rule(self, uuid: str, rule: FirewallFilterRule) -> dict:
        rule_dict = rule.dict(exclude_unset=True)
        return self.ff.set_rule(uuid, json=rule_dict)

    def toggle_rule(self, uuid: str, enabled: bool = None) -> dict:
        if enabled is None:
            current_rule = self.get_rule(uuid)
            enabled = not current_rule.enabled
        return self.ff.toggle_rule(uuid, json={"enabled": int(enabled)})

    def apply_changes(self) -> dict:
        return self.ff.apply()

    def create_savepoint(self) -> dict:
        return self.ff.savepoint()

    def cancel_rollback(self) -> dict:
        return self.ff.cancel_rollback()

    def list_rules(self) -> list[FirewallFilterRuleResponse]:
        response = self.ff.search_rule()
        if 'rows' in response:
            rules = []
            for rule_data in response['rows']:
                try:
                    rule = self._parse_rule_search_item(rule_data)
                    rules.append(rule)
                except Exception as error:
                    raise ParsingError("Failed to parse rule in list", rule_data, str(error))
            return rules
        return []

    def match_rule_by_attributes(self, **kwargs) -> list[dict[str, Any]]:
        all_rules = self.list_rules()
        matched_rules = []
        for rule in all_rules:
            rule_dict = rule.dict()
            rule_matched = True
            for key, value in kwargs.items():
                if rule_dict.get(key) != value:
                    rule_matched = False
                    break
            if rule_matched:
                matched_rules.append(rule_dict)
        return matched_rules

    @staticmethod
    def _transform_rule_response(rule_data: dict) -> dict:
        # Implement the logic to transform the API response to the Pydantic model format
        # This is a placeholder and should be implemented based on the actual API response structure
        return {
            "sequence": int(rule_data.get("sequence", 0)),
            "action": rule_data.get("action"),
            "quick": bool(int(rule_data.get("quick", 1))),
            "interface": rule_data.get("interface", "").split(","),
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

    @staticmethod
    def _parse_rule_search_item(rule_data: dict) -> FirewallFilterRuleResponse:
        # Implement the logic to parse the search result item
        # This is a placeholder and should be implemented based on the actual API response structure
        return FirewallFilterRuleResponse(
            uuid=rule_data.get("uuid", ""),
            sequence=int(rule_data.get("sequence", 0)),
            action=rule_data.get("action"),
            quick=bool(int(rule_data.get("quick", 1))),
            interface=rule_data.get("interface", "").split(","),
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
