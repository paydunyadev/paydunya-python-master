"""PAYDUNYA

PAYDUNYA Python client library.
Modules implemented: DirectPay, Invoice, and OPR
"""

__version__ = '1.0.6'
__author__ = "PAYDUNYA <paydunya@paydunya.com>"

import sys
import requests
try:
    import simplejson as json
except ImportError:
    import json

# runs in LIVE mode by defaults
debug = False
api_keys = {}

# PAYDUNYA HTTP API version
API_VERSION = 'v1'

SERVER = "app.paydunya.com"

# Sandbox Endpoint
SANDBOX_ENDPOINT = "https://%s/sandbox-api/%s/" % (SERVER, API_VERSION)

# Live Endpoint
LIVE_ENDPOINT = "https://%s/api/%s/" % (SERVER, API_VERSION)

# user-agent
PAYDUNYA_USER_AGENT = "paydunya-python/v%s" % __version__

# fixme: find a better way of 'self' referencing
__MODULE__ = sys.modules[__name__]


class PaydunyaError(Exception):
    """Base Exception class"""
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Store(object):
    """PAYDUNYA Store

    Creates a store object for PAYDUNYA transactions
    """
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.tagline = kwargs.get('tagline', None)
        self.postal_address = kwargs.get('postal_address', None)
        self.phone_number = kwargs.get('phone_number', None)
        self.website_url = kwargs.get('website_url', None)
        self.logo_url = kwargs.get('logo_url', None)

    @property
    def info(self):
        """Returns the store information

        What this does is simply return the store object's attributes
        """
        return self.__dict__


class Payment(object):
    """Base class for other PAYDUNYA classes"""

    def __init__(self):
        """Base class for all the other payment libraries"""
        # request headers
        self._headers = {
            'User-Agent': PAYDUNYA_USER_AGENT,
            "Content-Type": "application/json"
        }
        # response object
        self._response = None
        # data to send to server
        self._data = None
        self.store = Store(name=None)

    def _process(self, resource=None, data={}):
        """Processes the current transaction

        Sends an HTTP request to the PAYDUNYA API server
        """
        # use object's data if no data is passed
        _data = data or self._data
        rsc_url = self.get_rsc_endpoint(resource)
        if _data:
            req = requests.post(rsc_url, data=json.dumps(_data),
                                headers=self.headers)
        else:
            req = requests.get(rsc_url, params=_data,
                               headers=self.headers)
        if req.status_code == 200:
            self._response = json.loads(req.text)
            if int(self._response['response_code']) == 00:
                return (True, self._response)
            else:
                return (False, self._response['response_text'])
        else:
            return (500, "Request Failed")

    @property
    def headers(self):
        """Returns the client's Request headers"""
        return dict(self._config, **self._headers)

    def add_header(self, header):
        """Add a custom HTTP header to the client's request headers"""
        if type(header) is dict:
            self._headers.update(header)
        else:
            raise ValueError(
                "Dictionary expected, got '%s' instead" % type(header)
            )

    def get_rsc_endpoint(self, rsc):
        """Returns the HTTP API URL for current payment transaction"""
        if self.debug:
            return SANDBOX_ENDPOINT + rsc
        return LIVE_ENDPOINT + rsc

    @property
    def debug(self):
        """Returns the current transaction mode"""
        return __MODULE__.debug

    @property
    def _config(self):
        _m = __MODULE__
        return {
            'PAYDUNYA-MASTER-KEY': _m.api_keys.get('PAYDUNYA-MASTER-KEY'),
            'PAYDUNYA-PRIVATE-KEY': _m.api_keys.get('PAYDUNYA-PRIVATE-KEY'),
            'PAYDUNYA-TOKEN': _m.api_keys.get('PAYDUNYA-TOKEN')
        }


# moved here so the modules that depend on the 'Payment' class will work
from .invoice import Invoice, InvoiceItem
from .direct_payments import DirectPay
from .opr import OPR

__all__ = [
    Store.__name__,
    Payment.__name__,
    Invoice.__name__,
    InvoiceItem.__name__,
    DirectPay.__name__,
    OPR.__name__
]
