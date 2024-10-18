from enum import Enum
from typing import Optional
from pydantic import BaseModel


class Action(str, Enum):
    PASS = "pass"
    BLOCK = "block"
    REJECT = "reject"


class Direction(str, Enum):
    IN = "in"
    OUT = "out"


class IPProtocol(str, Enum):
    INET = "inet"
    INET6 = "inet6"


class Protocol(str, Enum):
    ANY = "any"
    TCP = "TCP"
    UDP = "UDP"
    ICMP = "ICMP"
    # Add other protocols as needed


class FirewallFilterRule(BaseModel):
    sequence: int
    action: Action
    quick: bool = True
    interface: list[str]
    direction: Direction
    ipprotocol: IPProtocol
    protocol: Protocol
    source_net: str
    source_not: bool = False
    source_port: Optional[str] = None
    destination_net: str
    destination_not: bool = False
    destination_port: Optional[str] = None
    gateway: Optional[str] = None
    description: Optional[str] = None
    enabled: bool = True
    log: bool = False


class FirewallFilterRuleResponse(FirewallFilterRule):
    uuid: str
