import unittest
import paydunya
from . import PAYDUNYA_ACCESS_TOKENS

paydunya.debug = True
paydunya.api_keys = PAYDUNYA_ACCESS_TOKENS


class TestOPR(unittest.TestCase):
    def setUp(self):
        self.opr_data = {'account_alias': '774563209',
                         'description': 'Hello World',
                         'total_amount': 345}
        store = paydunya.Store(name="Event Shop")
        self.opr = paydunya.OPR(self.opr_data, store)

    def tearDown(self):
        self.opr = None

    def test_opr_create(self):
        status, resp = self.opr.create()
        self.assertTrue(status)

        status, _ = self.opr.create(self.opr_data)
        self.assertTrue(status)

    def test_opr_charge(self):
        status, response = self.opr.create()
        token = response['token']
        status, _ = self.opr.charge({'token': token,
                                     'confirm_token': "56Y8"})
        # request should because the token and
        # confirm_token combination are wrong
        self.assertFalse(status)

if __name__ == '__main__':
    unittest.main()
