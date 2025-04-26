from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, IPvAnyAddress

class DhcpLeaseType(str, Enum):
    """DHCP Lease Type Enum"""
    DYNAMIC = "dynamic"
    STATIC = "static"

class DhcpLeaseStatus(str, Enum):
    """DHCP Lease Status Enum"""
    ONLINE = "online"
    OFFLINE = "offline"

class DhcpLease(BaseModel):
    """Pydantic model for a single DHCP lease entry."""
    address: IPvAnyAddress
    starts: str  # Keeping as string due to potential empty value for static
    ends: str    # Keeping as string due to potential empty value for static
    cltt: Optional[int] = None # Client last transaction time (epoch)
    binding: Optional[str] = None
    uid: Optional[str] = None
    client_hostname: Optional[str] = Field(None, alias="client-hostname")
    type: DhcpLeaseType
    status: DhcpLeaseStatus
    descr: str
    mac: str # Could add validator for MAC format if needed: Field(..., pattern=r"^[0-9A-Fa-f]{2}(:[0-9A-Fa-f]{2}){5}$")
    hostname: str # Resolved hostname (may be empty)
    state: str # Internal lease state
    man: str # Manufacturer (may be empty)
    interface: str = Field(..., alias="if")
    interface_description: str = Field(..., alias="if_descr")

    class Config:
        allow_population_by_field_name = True # Allows using 'if' and 'if_descr' directly if needed
        use_enum_values = True # Ensure enum values are used when exporting

class DhcpLeaseResponse(BaseModel):
    """Pydantic model for the DHCP lease API response."""
    total: int
    row_count: int = Field(..., alias="rowCount")
    current: int
    rows: list[DhcpLease]
    interfaces: dict[str, str]

    class Config:
        allow_population_by_field_name = True
