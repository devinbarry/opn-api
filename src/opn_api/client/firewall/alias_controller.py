from opn_api.api.core.firewall import FirewallAlias, FirewallAliasUtil
from opn_api.models.firewall_alias import (
    AliasType,
    ProtocolType,
    FirewallAliasCreate,
    FirewallAliasUpdate,
    FirewallAliasResponse,
)
from opn_api.exceptions import ParsingError


class AliasController:
    def __init__(self, client):
        self.fa = FirewallAlias(client)
        self.fau = FirewallAliasUtil(client)

    def list(self) -> list[FirewallAliasResponse]:
        search_results = self.fa.search_item()
        aliases = []
        for alias_data in search_results.get('rows', []):
            try:
                alias = self._parse_alias_search_item(alias_data)
                aliases.append(alias)
            except Exception as error:
                raise ParsingError("Failed to parse alias in list", alias_data, str(error))
        return aliases

    def get(self, uuid: str) -> FirewallAliasResponse:
        query_response = self.fa.get_item(uuid)
        if 'alias' in query_response:
            try:
                alias_data = query_response['alias']
                model_data = self._transform_alias_response(alias_data)
                alias = FirewallAliasResponse(uuid=uuid, **model_data)
                return alias
            except Exception as error:
                raise ParsingError(
                    f"Failed to parse the alias with UUID: {uuid}", query_response['alias'], str(error)
                )
        raise ValueError(f"No alias found with UUID: {uuid}")

    def get_uuid(self, name: str) -> str:
        search_results = self.fa.get_uuid_for_name(name)
        if 'uuid' in search_results:
            return search_results['uuid']
        raise ValueError(f"No alias found with name: {name}")

    def toggle(self, uuid: str, enabled: bool = None) -> dict:
        if enabled is None:
            current_alias = self.get(uuid)
            enabled = not current_alias.enabled
        return self.fa.toggle_item(uuid, body={"enabled": int(enabled)})

    def delete(self, uuid: str) -> dict:
        return self.fa.del_item(uuid)

    def add(self, alias: FirewallAliasCreate) -> dict:
        request_body = self._prepare_alias_body(alias)
        return self.fa.add_item(body=request_body)

    def set(self, alias: FirewallAliasUpdate) -> dict:
        request_body = self._prepare_alias_body(alias)
        return self.fa.set_item(alias.uuid, body=request_body)

    def apply_changes(self) -> dict:
        return self.fa.reconfigure()

    @staticmethod
    def _prepare_alias_body(alias: FirewallAliasCreate | FirewallAliasUpdate) -> dict:
        alias_content = "\n".join(map(str, alias.content or []))
        return {
            "alias": {
                "name": alias.name,
                "type": alias.type.value,
                "description": alias.description or "",
                "updatefreq": alias.update_freq or "",
                "counters": alias.counters or "",
                "proto": alias.proto.value if alias.proto else "",
                "content": alias_content,
                "enabled": str(int(alias.enabled)),
            }
        }

    @staticmethod
    def _transform_alias_response(alias_data: dict) -> dict:
        name = alias_data.get("name", "")
        description = alias_data.get("description", "")
        enabled = bool(int(alias_data.get('enabled', '1')))

        counters = alias_data.get("counters", "")
        updatefreq = alias_data.get("updatefreq", "")

        # Get 'type' field
        alias_type = None
        type_dict = alias_data.get("type", {})
        for key, value in type_dict.items():
            if value.get("selected") == 1:
                alias_type = AliasType(key.lower())
                break

        # Get 'proto' field
        proto = None
        proto_dict = alias_data.get("proto", {})
        for key, value in proto_dict.items():
            if value.get("selected") == 1:
                proto = ProtocolType(key)
                break

        # Get 'content' field
        content_list = []
        content_dict = alias_data.get("content", {})
        for key, value in content_dict.items():
            if value.get("selected") == 1:
                content_list.append(value.get("value"))

        return {
            "name": name,
            "type": alias_type,
            "description": description,
            "update_freq": updatefreq,
            "counters": counters,
            "proto": proto,
            "content": content_list,
            "enabled": enabled,
        }

    @staticmethod
    def _parse_alias_search_item(alias_data: dict) -> FirewallAliasResponse:
        uuid = alias_data.get("uuid", "")
        name = alias_data.get("name", "")
        description = alias_data.get("description", "")
        enabled = bool(int(alias_data.get("enabled", "1")))
        content = alias_data.get("content", "")
        content_list = content.split('\n') if content else []
        alias_type_str = alias_data.get("type", "")
        alias_type = AliasType(alias_type_str.lower().replace('(s)', '').strip())

        return FirewallAliasResponse(
            uuid=uuid,
            name=name,
            type=alias_type,
            description=description,
            update_freq=None,
            counters=None,
            proto=None,
            content=content_list,
            enabled=enabled,
        )
