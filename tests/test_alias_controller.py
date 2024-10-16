import uuid
import unittest
from unittest.mock import Mock
from opn_api.models.firewall_alias import AliasType
from opn_api.client.firewall.alias_controller import AliasController


class TestAlias(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.alias = AliasController(self.mock_client)

    def test_list(self):
        mock_response = {'rows': [{'name': 'test_alias'}]}
        self.alias.fa.search_item = Mock(return_value=mock_response)
        result = self.alias.list()
        self.assertEqual(result, [{'name': 'test_alias'}])

    def test_list_empty(self):
        self.alias.fa.search_item = Mock(return_value={})
        result = self.alias.list()
        self.assertEqual(result, [])

    def test_get(self):
        mock_response = {
            'alias': {
                'name': 'test_alias',
                'description': 'Test description',
                'type': {'HOST': {'selected': 1}},
                'proto': {'TCP': {'selected': 1}},
                'content': {
                    '192.168.1.1': {'selected': 1, 'value': '192.168.1.1'}
                },
                'enabled': '1'
            }
        }
        self.alias.fa.get_item = Mock(return_value=mock_response)
        result = self.alias.get('test_uuid')
        self.assertEqual(result['name'], 'test_alias')
        self.assertEqual(result['description'], 'Test description')
        self.assertEqual(result['type'], 'HOST')
        self.assertEqual(result['proto'], 'TCP')
        self.assertEqual(result['content'], ['192.168.1.1'])
        self.assertTrue(result['enabled'])

    def test_get_missing_description(self):
        mock_response = {
            'alias': {
                'name': 'test_alias',
                'type': {'HOST': {'selected': 1}},
                'proto': {'TCP': {'selected': 1}},
                'content': {
                    '192.168.1.1': {'selected': 1, 'value': '192.168.1.1'}
                },
                'enabled': '1'
            }
        }
        self.alias.fa.get_item = Mock(return_value=mock_response)
        result = self.alias.get('test_uuid')
        self.assertEqual(result['name'], 'test_alias')
        self.assertEqual(result['description'], '')
        self.assertEqual(result['type'], 'HOST')
        self.assertEqual(result['proto'], 'TCP')
        self.assertEqual(result['content'], ['192.168.1.1'])
        self.assertTrue(result['enabled'])

    def test_get_content_without_value(self):
        mock_response = {
            'alias': {
                'name': 'test_alias',
                'type': {'HOST': {'selected': 1}},
                'proto': {'TCP': {'selected': 1}},
                'content': {
                    '192.168.1.1': {'selected': 1, 'value': '192.168.1.1'},
                    '192.168.1.2': {'selected': 1, 'value': '192.168.1.2'}
                },
                'enabled': '1'
            }
        }
        self.alias.fa.get_item = Mock(return_value=mock_response)
        result = self.alias.get('test_uuid')
        self.assertEqual(result['content'], ['192.168.1.1', '192.168.1.2'])

    def test_get_not_found(self):
        self.alias.fa.get_item = Mock(return_value={})
        with self.assertRaises(ValueError):
            self.alias.get('non_existent_uuid')

    def test_get_uuid(self):
        mock_response = {'uuid': 'test_uuid'}
        self.alias.fa.get_uuid_for_name = Mock(return_value=mock_response)
        result = self.alias.get_uuid('test_alias')
        self.assertEqual(result, 'test_uuid')

    def test_get_uuid_not_found(self):
        self.alias.fa.get_uuid_for_name = Mock(return_value={})
        with self.assertRaises(ValueError):
            self.alias.get_uuid('non_existent_alias')

    def test_toggle(self):
        self.alias.get = Mock(return_value={'enabled': True})
        self.alias.fa.toggle_item = Mock(return_value={'result': 'ok'})
        result = self.alias.toggle('test_uuid')
        self.alias.fa.toggle_item.assert_called_with('test_uuid', json={'enabled': 0})
        self.assertEqual(result, {'result': 'ok'})

    def test_delete(self):
        self.alias.fa.del_item = Mock(return_value={'result': 'ok'})
        result = self.alias.delete('test_uuid')
        self.alias.fa.del_item.assert_called_with('test_uuid')
        self.assertEqual(result, {'result': 'ok'})

    def test_add(self):
        response = {'result': 'saved', 'uuid': str(uuid.uuid4())}
        self.alias.fa.add_item = Mock(return_value=response)
        result = self.alias.add('test_alias', AliasType.HOST, content=['192.168.1.1'])
        self.alias.fa.add_item.assert_called_once()
        self.assertEqual(result, {'result': 'ok'})

    def test_set(self):
        self.alias.fa.set_item = Mock(return_value={'result': 'ok'})
        result = self.alias.set('test_uuid', 'test_alias', AliasType.HOST, content=['192.168.1.1'])
        self.alias.fa.set_item.assert_called_once()
        self.assertEqual(result, {'result': 'ok'})

    def test_apply_changes(self):
        self.alias.fa.reconfigure = Mock(return_value={'result': 'ok'})
        result = self.alias.apply_changes()
        self.alias.fa.reconfigure.assert_called_once()
        self.assertEqual(result, {'result': 'ok'})
