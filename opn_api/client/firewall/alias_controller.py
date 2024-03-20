from opnsense_api.util import AliasType, ProtocolType
from opnsense_api.util.parse import parse_query_response_alias


class Alias:

    def __init__(self, client):
        self.fa = FirewallAlias(client)
        self.fau = FirewallAliasUtil(client)

    def list(self) -> list:
        search_results = self.fa.search_item()
        if 'rows' in search_results:
            return search_results['rows']
        return []

    def get(self, uuid: str) -> dict:
        query_response = self.fa.get_item(uuid)
        if 'alias' in query_response:
            try:
                return parse_query_response_alias(query_response['alias'])
            except Exception as error:
                raise Exception(f"Failed to parse the alias with UUID: {uuid}\nException: {error.with_traceback()}")

    def get_uuid(self, name: str) -> str | None:
        search_results = self.device._authenticated_request("GET", f"firewall/alias/getAliasUUID/{name}")
        if 'uuid' in search_results:
            return search_results['uuid']
        return None

    def toggle(self, uuid, enabled=None):
        if enabled is None:
            enabled = bool(int(self.get_alias(uuid)['enabled']))
        return self.device._authenticated_request("POST", f"firewall/alias/toggleItem/{uuid}?enabled={not enabled}")

    def delete(self, uuid):
        return self.device._authenticated_request("POST", f"firewall/alias/delItem/{uuid}")

    def add(self, name: str, alias_type: AliasType, description: str = "", update_freq: str = "", counters: str = "",
            proto: ProtocolType = None, content=None, enabled: bool = True):
        if content is None:
            content = []

        protocol_type = ""
        if proto is not None:
            protocol_type = proto.value

        alias_content = ""
        if len(content) > 0:
            content = [str(item) for item in content]
            alias_content = "\n".join(content)

        request_body = {
            "alias": {
                "name": name,
                "type": alias_type.value,
                "description": description,
                "updatefreq": update_freq,
                "counters": counters,
                "proto": protocol_type,
                "content": alias_content,
                "enabled": str(int(enabled))
            }
        }
        return self.device._authenticated_request("POST", f"firewall/alias/addItem", body=request_body)

    def set(self, uuid: str, name: str, alias_type: AliasType, description: str = "", update_freq: str = "",
            counters: str = "", proto: ProtocolType = None, content=None, enabled: bool = True):
        protocol_type = ""
        if proto is not None:
            protocol_type = proto.value

        alias_content = ""
        if content is not None:
            if len(content) > 0:
                content = [str(item) for item in content]
                alias_content = "\n".join(content)

        request_body = {
            "alias": {
                "name": name,
                "type": alias_type.value,
                "description": description,
                "updatefreq": update_freq,
                "counters": counters,
                "proto": protocol_type,
                "content": alias_content,
                "enabled": str(int(enabled))
            }
        }
        return self.device._authenticated_request("POST", f"firewall/alias/setItem/{uuid}", body=request_body)
