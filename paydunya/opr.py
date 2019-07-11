"""PAYDUNYA Onsite Payments Request"""
from . import Payment


class OPR(Payment):
    """Onsite Payment Request"""
    def __init__(self, data={}, store=None):
        self._opr_data = self._build_opr_data(data, store)
        super(OPR, self).__init__()
        if store:
            self.store = store

    def _build_opr_data(self, data, store):
        """Returns a well formatted OPR data"""
        return {
            "invoice_data": {
                "invoice": {
                    "total_amount": data.get("total_amount"),
                    "description": data.get("description")
                },
                "store": store.info
            },
            "opr_data": {
                "account_alias": data.get("account_alias")
            }
        }

    def create(self, data={}, store=None):
        """Initiazes an OPR

        First step in the OPR process is to create the OPR request.
        Returns the OPR token
        """
        _store = store or self.store
        _data = self._build_opr_data(data, _store) if data else self._opr_data
        return self._process('opr/create', _data)

    def charge(self, data):
        """Second stage of an OPR request"""
        token = data.get("token", self._response["token"])
        data = {
            "token": token,
            "confirm_token": data.get("confirm_token")
        }
        return self._process('opr/charge', data)
