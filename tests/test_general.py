import unittest
import paydunya
from . import PAYDUNYA_ACCESS_TOKENS

paydunya.debug = True
paydunya.api_keys = PAYDUNYA_ACCESS_TOKENS


class TestGeneral(unittest.TestCase):
    """General/Miscellaneous tests"""
    def setUp(self):
        # Your PAYDUNYA developer tokens
        self.store = paydunya.Store(name="Fabrice Accessoires")
        self.opr_data = {'total_amount': 215000,
                         'description': "Samsung Galaxy S6",
                         "account_alias": "774563209"}
        self.opr = paydunya.OPR(self.opr_data, self.store)

    def tearDown(self):
        self.opr = None
        self.store = None
        self.opr_data = None

    def test_rsc_endpoints(self):
        endpoint = 'checkout-invoice/confirm/test_98567JGF'
        url = self.opr.get_rsc_endpoint(endpoint)
        self.assertTrue(url.startswith('https') and url.endswith(endpoint))

    def test_add_headers(self):
        header = {'Foo': 'Bar'}
        self.opr.add_header(header)
        self.assertTrue("Foo" in self.opr.headers.keys())
        self.assertFalse('FooBar' in self.opr.headers.keys())


if __name__ == '__main__':
    unittest.main()
