import uuid

test_uuid = str(uuid.uuid4())


def mock_get_uuid_for_name_data(name):
    return {"uuid": test_uuid}


def mock_get_geo_ip_data():
    return {"alias": {"geoip": {"url": "", "usages": 0, "address_count": 0}}}


def mock_get_table_size_data():
    return {
        "status": "ok",
        "size": 1000000,
        "used": 1811,
        "details": {
            "SubnetA": {"count": 1, "updated": "2024-01-01T11:49:05.361174"},
            "SubnetB": {"count": 1, "updated": "2024-01-01T11:49:05.366848"},
            "Device_A": {"count": 4, "updated": "2024-03-20T12:33:14.435029"},
            "Office2": {"count": 1, "updated": "2024-01-01T11:58:09.086308"},
            "RFC1918": {"count": 3, "updated": "2024-02-06T01:51:41.226413"},
            "Securelab": {"count": 1, "updated": "2024-02-08T11:01:19.231621"},
            "Wireguard_Client": {"count": 1, "updated": "2024-06-25T23:22:50.464222"},
            "__automatic_93fb8493_0": {"count": 8, "updated": None},
            "__lan_network": {"count": 1, "updated": None},
            "__lo0_network": {"count": 2, "updated": None},
            "__opt1_network": {"count": 1, "updated": None},
            "__opt2_network": {"count": 1, "updated": None},
            "__opt3_network": {"count": 1, "updated": None},
            "__opt4_network": {"count": 1, "updated": None},
            "__opt5_network": {"count": 1, "updated": None},
            "__opt6_network": {"count": 1, "updated": None},
            "__wan_network": {"count": 1, "updated": None},
            "bogons": {"count": 1777, "updated": None},
            "hass": {"count": 1, "updated": "2024-04-21T13:38:07.635399"},
            "iPhone15Pro": {"count": 1, "updated": "2024-06-02T16:08:09.750460"},
            "npia2002d": {"count": 1, "updated": "2024-07-18T02:32:56.505264"},
            "sshlockout": {"count": 0, "updated": None},
            "monitoring_tool": {"count": 1, "updated": "2024-02-07T03:30:04.629978"},
            "virusprot": {"count": 0, "updated": None},
        },
    }


def mock_list_categories_data():
    return {"rows": [{"uuid": test_uuid, "name": "Uptime Kuma", "color": "", "used": 0}]}


def mock_list_countries_data():
    return {
        "EU": {"name": "Unclassified", "region": "Europe"},
        "AD": {"name": "Andorra", "region": "Europe"},
        "AE": {"name": "United Arab Emirates", "region": "Asia"},
        "AF": {"name": "Afghanistan", "region": "Asia"},
        "AG": {"name": "Antigua & Barbuda", "region": "America"},
        "AI": {"name": "Anguilla", "region": "America"},
        "AL": {"name": "Albania", "region": "Europe"},
        "AM": {"name": "Armenia", "region": "Asia"},
        "AO": {"name": "Angola", "region": "Africa"},
        "AQ": {"name": "Antarctica", "region": "Antarctica"},
        "AR": {"name": "Argentina", "region": "America"},
        "AS": {"name": "Samoa (American)", "region": "Pacific"},
        "AT": {"name": "Austria", "region": "Europe"},
        "AU": {"name": "Australia", "region": "Australia"},
        "AW": {"name": "Aruba", "region": "America"},
    }


def mock_list_network_aliases_data():
    return {
        "SubnetA": {"name": "SubnetA", "description": "SubnetA subnet"},
        "SubnetB": {"name": "SubnetB", "description": "SubnetB subnet"},
        "Device_A": {"name": "Device_A", "description": "Device_A on various subnets"},
        "Office2": {"name": "Office2", "description": "Office2 subnet"},
        "RFC1918": {"name": "RFC1918", "description": "Private networks"},
        "Securelab": {"name": "Securelab", "description": "Securelab VM"},
        "Wireguard_Client": {"name": "Wireguard_Client", "description": "Wireguard client on user iPhone"},
        "__lan_network": {"name": "__lan_network", "description": "Engineering2 net"},
        "__lo0_network": {"name": "__lo0_network", "description": "Loopback net"},
        "__opt1_network": {"name": "__opt1_network", "description": "SubnetE net"},
        "__opt2_network": {"name": "__opt2_network", "description": "Switch2 net"},
        "__opt3_network": {"name": "__opt3_network", "description": "Unifi net"},
        "__opt4_network": {"name": "__opt4_network", "description": "IOT net"},
        "__opt5_network": {"name": "__opt5_network", "description": "Switch3 net"},
        "__opt6_network": {"name": "__opt6_network", "description": "UPS net"},
        "__wan_network": {"name": "__wan_network", "description": "WAN net"},
        "hass": {"name": "hass", "description": "Home Assistant VM"},
        "iPhone15Pro": {"name": "iPhone15Pro", "description": "Users Phone Device"},
        "npia2002d": {"name": "npia2002d", "description": "HP Laser Printer"},
        "monitoring_tool": {"name": "monitoring_tool", "description": "Monitoring Tool VM"},
    }


def mock_list_user_groups_data():
    return {"1999": {"name": "admins", "gid": "1999"}}
