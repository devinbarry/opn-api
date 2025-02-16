def mock_get_item_data(uuid):
    return {
        "alias": {
            "enabled": "1",
            "name": "HostA",
            "type": {
                "host": {"value": "Host(s)", "selected": 1},
                "network": {"value": "Network(s)", "selected": 0},
                "port": {"value": "Port(s)", "selected": 0},
                "url": {"value": "URL (IPs)", "selected": 0},
                "urltable": {"value": "URL Table (IPs)", "selected": 0},
                "geoip": {"value": "GeoIP", "selected": 0},
                "networkgroup": {"value": "Network group", "selected": 0},
                "mac": {"value": "MAC address", "selected": 0},
                "asn": {"value": "BGP ASN", "selected": 0},
                "dynipv6host": {"value": "Dynamic IPv6 Host", "selected": 0},
                "authgroup": {"value": "OpenVPN group", "selected": 0},
                "internal": {"value": "Internal (automatic)", "selected": 0},
                "external": {"value": "External (advanced)", "selected": 0},
            },
            "proto": {"IPv4": {"value": "IPv4", "selected": 0}, "IPv6": {"value": "IPv6", "selected": 0}},
            "interface": {
                "": {"value": "None", "selected": 1},
                "lan": {"value": "LAN net", "selected": 0},
                "opt4": {"value": "IOT", "selected": 0},
                "opt1": {"value": "SubnetE", "selected": 0},
                "opt2": {"value": "Switch2", "selected": 0},
                "opt5": {"value": "Switch3", "selected": 0},
                "opt3": {"value": "Unifi", "selected": 0},
                "opt6": {"value": "UPS", "selected": 0},
                "wan": {"value": "WAN net", "selected": 0},
            },
            "counters": "0",
            "updatefreq": "",
            "content": {
                "10.178.23.119": {"value": "10.178.23.119", "selected": 1},
                "10.198.180.120": {"value": "10.198.180.120", "selected": 1},
                "10.186.157.171": {"value": "10.186.157.171", "selected": 1},
                "10.16.197.238": {"value": "10.16.197.238", "selected": 1},
                "RFC1918": {"selected": 0, "value": "RFC1918", "description": "Private networks"},
                "HostA": {"selected": 0, "value": "HostA", "description": "HostA MBP on various subnets"},
                "monitoring_tool": {"selected": 0, "value": "monitoring_tool", "description": "Monitoring Tool VM"},
                "Secure_VM": {"selected": 0, "value": "Secure_VM", "description": "Secure VM"},
                "hass": {"selected": 0, "value": "hass", "description": "Home Assistant VM"},
                "bogons": {"selected": 0, "value": "bogons", "description": "bogon networks (internal)"},
                "bogonsv6": {"selected": 0, "value": "bogonsv6", "description": "bogon networks IPv6 (internal)"},
                "virusprot": {
                    "selected": 0,
                    "value": "virusprot",
                    "description": "overload table for rate limiting (internal)",
                },
                "sshlockout": {"selected": 0, "value": "sshlockout", "description": "abuse lockout table (internal)"},
                "__wan_network": {"selected": 0, "value": "__wan_network", "description": "WAN net"},
                "__lan_network": {"selected": 0, "value": "__lan_network", "description": "LAN net"},
                "__lo0_network": {"selected": 0, "value": "__lo0_network", "description": "Loopback net"},
                "__opt1_network": {"selected": 0, "value": "__opt1_network", "description": "SubnetE net"},
                "__opt2_network": {"selected": 0, "value": "__opt2_network", "description": "Switch2 net"},
                "__opt3_network": {"selected": 0, "value": "__opt3_network", "description": "Unifi net"},
                "__opt4_network": {"selected": 0, "value": "__opt4_network", "description": "IOT net"},
                "__opt5_network": {"selected": 0, "value": "__opt5_network", "description": "Switch3 net"},
                "__opt6_network": {"selected": 0, "value": "__opt6_network", "description": "UPS net"},
            },
            "categories": {"f04a0dac-798e-48b8-8ff5-3380a25c2e8c": {"value": "Uptime Kuma", "selected": 0}},
            "description": "HostA MBP on various subnets",
        }
    }
