from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class AliasType(Enum):
    HOST = "host"
    NETWORK = "network"
    PORT = "port"
    URL = "url"


class ProtocolType(Enum):
    IPV4 = "IPv4"
    IPV6 = "IPv6"


class FirewallAlias(BaseModel):
    """Base model for firewall alias"""
    name: str
    type: AliasType
    description: Optional[str] = ""
    content: list[str] = Field(default_factory=list)
    enabled: bool = True
    update_freq: Optional[str] = ""
    counters: Optional[str] = ""
    proto: Optional[ProtocolType] = None


class FirewallAliasCreate(FirewallAlias):
    """Model for creating a firewall alias"""
    pass


class FirewallAliasUpdate(FirewallAlias):
    """Model for updating a firewall alias"""
    uuid: str


class FirewallAliasResponse(FirewallAlias):
    """Model for firewall alias response"""
    uuid: str


class FirewallAliasToggle(BaseModel):
    """Model for toggling firewall alias"""
    uuid: str
    enabled: bool


class FirewallAliasDelete(BaseModel):
    """Model for deleting firewall alias"""
    uuid: str
