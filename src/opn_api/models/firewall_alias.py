from enum import StrEnum
from pydantic import BaseModel, Field, field_validator


class AliasType(StrEnum):
    """
    Enumeration of firewall alias types supported by OPNsense.

    Note: OPNsense changed the API response format for system-generated aliases in version 25.7:

    - OPNsense < 25.7: Returns display values like "internal (automatic)", "external (advanced)"
    - OPNsense >= 25.7: Returns literal values like "internal", "external"

    This library supports both formats for compatibility across all OPNsense versions.
    System-generated aliases include: bogons, bogonsv6, sshlockout, virusprot,
    __lan_network, __wan_network, and other interface network aliases.

    Reference: OPNsense 25.7 changelog - API grid return values now offer "%field" for display
    descriptions while "field" always contains the literal configuration value.
    """
    HOST = "host"
    NETWORK = "network"
    PORT = "port"
    URL = "url"
    GEOIP = "geoip"
    MAC = "mac"
    ASN = "asn"
    AUTH_GROUP = "auth_group"
    DYN_IPV6_HOST = "dynipv6host"
    # Modern format (OPNsense >= 25.7) - literal values for system-generated internal aliases
    INTERNAL = "internal"
    # Legacy format (OPNsense < 25.7) - display values for system-generated internal aliases
    INTERNAL_OLD = "internal (automatic)"
    # Modern format (OPNsense >= 25.7) - literal values for system-generated external aliases
    EXTERNAL = "external"
    # Legacy format (OPNsense < 25.7) - display values for system-generated external aliases
    EXTERNAL_OLD = "external (advanced)"


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

    @field_validator('proto', mode='before')
    @classmethod
    def validate_proto(cls, v):
        """
        Validates and normalizes the protocol field.

        The OPNsense API returns an empty string for aliases that don't have a protocol
        (e.g., port, url, mac, auth_group types). This validator converts empty strings
        to None to ensure proper Pydantic validation.
        """
        if v == "" or v is None:
            return None
        return v    


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
