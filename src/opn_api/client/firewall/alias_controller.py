from opn_api.util.parse import parse_query_response_alias
from opn_api.api.core.firewall import FirewallAlias, FirewallAliasUtil
from opn_api.models.firewall_alias import AliasType, ProtocolType
from opn_api.exceptions import ParsingError


class AliasController:
    def __init__(self, client):
        self.fa = FirewallAlias(client)
        self.fau = FirewallAliasUtil(client)

    def list(self) -> list:
        search_results = self.fa.search_item()
        return search_results.get('rows', [])

    def get(self, uuid: str) -> dict:
        query_response = self.fa.get_item(uuid)
        if 'alias' in query_response:
            try:
                return parse_query_response_alias(query_response['alias'])
            except Exception as error:
                raise ParsingError(f"Failed to parse the alias with UUID: {uuid}", query_response['alias'],
                                   str(error))
        raise ValueError(f"No alias found with UUID: {uuid}")

    def get_uuid(self, name: str) -> str:
        search_results = self.fa.get_uuid_for_name(name)
        if 'uuid' in search_results:
            return search_results['uuid']
        raise ValueError(f"No alias found with name: {name}")

    def toggle(self, uuid: str, enabled: bool = None) -> dict:
        if enabled is None:
            current_alias = self.get(uuid)
            enabled = not current_alias['enabled']
        return self.fa.toggle_item(uuid, json={"enabled": int(enabled)})

    def delete(self, uuid: str) -> dict:
        return self.fa.del_item(uuid)

    def add(self, name: str, alias_type: AliasType, description: str = "", update_freq: str = "", counters: str = "",
            proto: ProtocolType = None, content: list = None, enabled: bool = True) -> dict:
        request_body = self._prepare_alias_body(name, alias_type, description, update_freq, counters, proto, content,
                                                enabled)
        return self.fa.add_item(body=request_body)

    def set(self, uuid: str, name: str, alias_type: AliasType, description: str = "", update_freq: str = "",
            counters: str = "", proto: ProtocolType = None, content: list = None, enabled: bool = True) -> dict:
        request_body = self._prepare_alias_body(name, alias_type, description, update_freq, counters, proto, content,
                                                enabled)
        return self.fa.set_item(uuid, body=request_body)

    def apply_changes(self) -> dict:
        return self.fa.reconfigure()

    @staticmethod
    def _prepare_alias_body(name: str, alias_type: AliasType, description: str, update_freq: str, counters: str,
                            proto: ProtocolType, content: list, enabled: bool) -> dict:
        alias_content = "\n".join(map(str, content or []))
        return {
            "alias": {
                "name": name,
                "type": alias_type.value,
                "description": description,
                "updatefreq": update_freq,
                "counters": counters,
                "proto": proto.value if proto else "",
                "content": alias_content,
                "enabled": str(int(enabled))
            }
        }
