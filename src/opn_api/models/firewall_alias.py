from enum import Enum
from typing import Optional
from pydantic import BaseModel


class AliasType(Enum):
    HOST = "host"
    NETWORK = "network"
    PORT = "port"
    URL = "url"


class ProtocolType(Enum):
    IPV4 = "IPv4"
    IPV6 = "IPv6"


class FirewallAlias(BaseModel):
    """validating the firewall alias"""
    name: str
    alias_type: AliasType
    content: list[str]
    description: Optional[str]
    enabled: bool


class FirewallAliasUpdate(FirewallAlias):
    """validating the firewall alias update"""
    uuid: str
    name: str
    alias_type: AliasType
    content: list[str]
    description: Optional[str]
    enabled: bool


class FirewallAliasCreate(FirewallAlias):
    """validating the firewall alias create"""
    name: str
    alias_type: AliasType
    content: list[str]
    description: Optional[str]
    enabled: bool
