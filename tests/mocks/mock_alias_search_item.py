def mock_search_item_data():
    return {
        'rows': [
            {
                'uuid': 'bogons',
                'enabled': '1',
                'name': 'bogons',
                'description': 'bogon networks (internal)',
                'type': 'External (advanced)',
                'content': '',
                'current_items': '1777',
                'last_updated': '',
                'categories_uuid': []
            },
            {
                'uuid': 'bogonsv6',
                'enabled': '1',
                'name': 'bogonsv6',
                'description': 'bogon networks IPv6 (internal)',
                'type': 'External (advanced)',
                'content': '',
                'current_items': '',
                'last_updated': '',
                'categories_uuid': []
            },
            {
                'uuid': '2ccd1d76-d80e-467c-8346-c164fd4a7408',
                'enabled': '1',
                'name': 'Network_A',
                'description': 'Network_A subnet',
                'type': 'Network(s)',
                'content': '10.178.23.0/24',
                'current_items': '1',
                'last_updated': '2024-01-01T11:49:05.361174',
                'categories_uuid': []
            },
            {
                'uuid': 'd0170249-abfe-476f-972c-4d6e2dc63c45',
                'enabled': '1',
                'name': 'Network_B',
                'description': 'Network_B subnet',
                'type': 'Network(s)',
                'content': '10.31.81.0/24',
                'current_items': '1',
                'last_updated': '2024-01-01T11:49:05.366848',
                'categories_uuid': []
            },
            {
                'uuid': '8099d776-1fac-4977-acf7-c2318cc4c7ae',
                'enabled': '1',
                'name': 'Home_VM',
                'description': 'Home Assistant VM',
                'type': 'Host(s)',
                'content': '10.16.16.100',
                'current_items': '1',
                'last_updated': '2024-04-21T13:38:07.635399',
                'categories_uuid': []
            },
            {
                'uuid': '72407b6f-f891-4d61-94bf-0f65ad36dd79',
                'enabled': '1',
                'name': 'Phone_Device',
                'description': 'Kates iPhone',
                'type': 'Host(s)',
                'content': '10.16.16.111',
                'current_items': '1',
                'last_updated': '2024-06-02T16:08:09.750460',
                'categories_uuid': []
            },
            {
                'uuid': 'c457be12-c921-486f-81e4-f0d2b3315bf0',
                'enabled': '1',
                'name': 'Device_A',
                'description': 'Device_A on various subnets',
                'type': 'Host(s)',
                'content': '10.200.0.12\n10.200.0.13\n10.31.81.40\n10.31.82.12',
                'current_items': '4',
                'last_updated': '2024-03-20T12:33:14.435029',
                'categories_uuid': []
            },
            {
                'uuid': '3e618775-6dd0-4cbe-9e86-ad7e59cfce0e',
                'enabled': '1',
                'name': 'Printer_Device',
                'description': 'Network Printer',
                'type': 'Host(s)',
                'content': '10.16.16.105',
                'current_items': '1',
                'last_updated': '2024-07-18T02:32:56.505264',
                'categories_uuid': []
            },
            {
                'uuid': 'f5286def-5e74-4c0b-91dd-458c0dafb5d0',
                'enabled': '1',
                'name': 'Network_C',
                'description': 'Network_C subnet',
                'type': 'Network(s)',
                'content': '172.20.24.0/24',
                'current_items': '1',
                'last_updated': '2024-01-01T11:58:09.086308',
                'categories_uuid': []
            },
            {
                'uuid': '07d836e7-355e-4df9-bccb-f5f32b9f14c2',
                'enabled': '1',
                'name': 'Private_Networks',
                'description': 'Private networks',
                'type': 'Network(s)',
                'content': '192.168.0.0/16\n172.16.0.0/12\n10.0.0.0/8',
                'current_items': '3',
                'last_updated': '2024-02-06T01:51:41.226413',
                'categories_uuid': []
            },
            {
                'uuid': '78d907a6-2fe6-4ce7-932e-048962ffce6d',
                'enabled': '1',
                'name': 'Secure_VM',
                'description': 'Secure VM',
                'type': 'Host(s)',
                'content': '172.20.23.135',
                'current_items': '1',
                'last_updated': '2024-02-08T11:01:19.231621',
                'categories_uuid': []
            },
            {
                'uuid': 'sshlockout',
                'enabled': '1',
                'name': 'sshlockout',
                'description': 'Abuse lockout table (internal)',
                'type': 'External (advanced)',
                'content': '',
                'current_items': '0',
                'last_updated': '',
                'categories_uuid': []
            },
            {
                'uuid': 'd0a5d458-3557-4e7c-ac17-a0db1f300f27',
                'enabled': '1',
                'name': 'VM_Monitor',
                'description': 'Monitoring VM',
                'type': 'Host(s)',
                'content': '172.20.24.150',
                'current_items': '1',
                'last_updated': '2024-02-07T03:30:04.629978',
                'categories_uuid': []
            },
            {
                'uuid': 'virusprot',
                'enabled': '1',
                'name': 'virusprot',
                'description': 'Overload table for rate limiting (internal)',
                'type': 'External (advanced)',
                'content': '',
                'current_items': '0',
                'last_updated': '',
                'categories_uuid': []
            },
            {
                'uuid': 'ddc9a6b5-e0d6-443e-b324-e039761fbc3f',
                'enabled': '1',
                'name': 'Wireguard_Client',
                'description': 'Wireguard client on device',
                'type': 'Host(s)',
                'content': '10.5.204.2',
                'current_items': '1',
                'last_updated': '2024-06-25T23:22:50.464222',
                'categories_uuid': []
            },
            {
                'uuid': '__lan_network',
                'enabled': '1',
                'name': '__lan_network',
                'description': 'LAN network',
                'type': 'Internal (automatic)',
                'content': '',
                'current_items': '1',
                'last_updated': '',
                'categories_uuid': []
            },
            {
                'uuid': '__lo0_network',
                'enabled': '1',
                'name': '__lo0_network',
                'description': 'Loopback network',
                'type': 'Internal (automatic)',
                'content': '',
                'current_items': '2',
                'last_updated': '',
                'categories_uuid': []
            },
            {
                'uuid': '__opt1_network',
                'enabled': '1',
                'name': '__opt1_network',
                'description': 'Opt1 network',
                'type': 'Internal (automatic)',
                'content': '',
                'current_items': '1',
                'last_updated': '',
                'categories_uuid': []
            },
            {
                'uuid': '__opt2_network',
                'enabled': '1',
                'name': '__opt2_network',
                'description': 'Opt2 network',
                'type': 'Internal (automatic)',
                'content': '',
                'current_items': '1',
                'last_updated': '',
                'categories_uuid': []
            },
            {
                'uuid': '__opt3_network',
                'enabled': '1',
                'name': '__opt3_network',
                'description': 'Opt3 network',
                'type': 'Internal (automatic)',
                'content': '',
                'current_items': '1',
                'last_updated': '',
                'categories_uuid': []
            },
            {
                'uuid': '__opt4_network',
                'enabled': '1',
                'name': '__opt4_network',
                'description': 'IOT network',
                'type': 'Internal (automatic)',
                'content': '',
                'current_items': '1',
                'last_updated': '',
                'categories_uuid': []
            },
            {
                'uuid': '__opt5_network',
                'enabled': '1',
                'name': '__opt5_network',
                'description': 'Opt5 network',
                'type': 'Internal (automatic)',
                'content': '',
                'current_items': '1',
                'last_updated': '',
                'categories_uuid': []
            },
            {
                'uuid': '__opt6_network',
                'enabled': '1',
                'name': '__opt6_network',
                'description': 'UPS network',
                'type': 'Internal (automatic)',
                'content': '',
                'current_items': '1',
                'last_updated': '',
                'categories_uuid': []
            },
            {
                'uuid': '__wan_network',
                'enabled': '1',
                'name': '__wan_network',
                'description': 'WAN network',
                'type': 'Internal (automatic)',
                'content': '',
                'current_items': '1',
                'last_updated': '',
                'categories_uuid': []
            }
        ],
        'rowCount': 24,
        'total': 24,
        'current': 1
    }
