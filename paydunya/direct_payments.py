"""PAYDUNYA DirectPay"""
from . import Payment

class DirectPay(Payment):
    """Directpay processing class

    Receipient account_info format:
    '{
       "account_alias" : "774563209",
       "amount" : 215000
    }'
    """
    def __init__(self, account_alias=None, amount=None):
        self.transaction = {
            'account_alias': account_alias,
            'amount': amount
        }
        super(DirectPay, self).__init__()

    def process(self, transaction=None):
        """Process the transaction"""
        return self._process('direct-pay/credit-account',
                             transaction or self.transaction)
