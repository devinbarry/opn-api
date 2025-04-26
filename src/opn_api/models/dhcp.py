import arrow
from dateutil import tz
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, IPvAnyAddress, field_validator


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
    starts: datetime | None
    ends: datetime | None
    cltt: int | None = None # Client last transaction time (epoch)
    binding: str | None = None
    uid: str | None = None
    client_hostname: str | None = Field(None, alias="client-hostname")
    type: DhcpLeaseType
    status: DhcpLeaseStatus
    descr: str
    mac: str
    hostname: str # Resolved hostname (may be empty)
    state: str # Internal lease state
    man: str # Manufacturer (may be empty)
    interface: str = Field(..., alias="if")
    interface_description: str = Field(..., alias="if_descr")

    @field_validator("starts", "ends", mode='before')
    @classmethod
    def parse_datetime(cls, value):
        if value in (None, ""):
            return None
        return arrow.get(value, 'YYYY/MM/DD HH:mm:ss', tzinfo=tz.gettz('Europe/London')).datetime


class DhcpLeaseResponse(BaseModel):
    """Pydantic model for the DHCP lease API response."""
    total: int
    row_count: int = Field(..., alias="rowCount")
    current: int
    rows: list[DhcpLease]
    interfaces: dict[str, str]
