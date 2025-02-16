from enum import StrEnum
from pydantic import BaseModel, Field


class AliasType(StrEnum):
    HOST = "host"
    NETWORK = "network"
    PORT = "port"
    URL = "url"
    GEOIP = "geoip"
    MAC = "mac"
    ASN = "asn"
    AUTH_GROUP = "auth_group"
    DYN_IPV6_HOST = "dynipv6host"
    INTERNAL = "internal (automatic)"
    EXTERNAL = "external (advanced)"


class ProtocolType(StrEnum):
    IPV4 = "IPv4"
    IPV6 = "IPv6"


class FirewallAlias(BaseModel):
    """Base model for firewall alias"""

    name: str
    type: AliasType
    description: str = ""
    content: list[str] = Field(default_factory=list)
    enabled: bool = True
    update_freq: str = Field(default="", description="Update frequency for dynamic aliases")
    counters: str = ""
    proto: ProtocolType | None = None


class FirewallAliasCreate(FirewallAlias):
    """
    Model for creating a firewall alias.
    Inherits all fields from FirewallAlias but doesn't require a UUID.
    """

    pass


class FirewallAliasUpdate(FirewallAlias):
    """
    Model for updating a firewall alias.
    Inherits all fields from FirewallAlias and requires a UUID.
    """

    uuid: str


class FirewallAliasResponse(FirewallAlias):
    """
    Model for firewall alias response.
    Includes all FirewallAlias fields plus a UUID.
    """

    uuid: str


class FirewallAliasToggle(BaseModel):
    """Model for toggling firewall alias"""

    uuid: str
    enabled: bool


class FirewallAliasDelete(BaseModel):
    """Model for deleting firewall alias"""

    uuid: str
