from opn_api.factories.code_generator.puppet_code_fragment import PuppetCodeFragmentFactory
from opn_api.tests.base import BaseTestCase
from opn_api.exceptions.factory import FactoryException


class TestPuppetCodeFragmentTypeFactory(BaseTestCase):
    def setUp(self):
        self._factory = PuppetCodeFragmentFactory()
        self._unknown_key = "unknown_key"

    def test_unknown_key(self):
        self.assertRaises(FactoryException, self._factory._get_class, self._unknown_key)
