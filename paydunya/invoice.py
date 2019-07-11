"""PAYDUNYA Invoice"""
from . import Payment
from collections import namedtuple

InvoiceItem = namedtuple('InvoiceItem', 'name quantity unit_price \
                             total_price description')


class Invoice(Payment):
    """Payment invoice"""

    def __init__(self, store=None):
        """Create an invoice

        Accepts list of store object as initial parameter and
        a dictionary of tokens for accessing the PAYDUNYA API
        """
        self.cancel_url = None
        self.return_url = None
        self.callback_url = None
        self.description = None
        self.items = {}
        self.total_amount = 0
        self.custom_data = {}
        self.taxes = {}
        self.channels = []
        super(Invoice, self).__init__()
        if store:
            self.store = store

    def create(self, items=[], taxes=[], custom_data=[]):
        """Adds the items to the invoice

        Format of 'items':
        [
         InvoiceItem(
             name="VIP Ticket",
             quantity= 2,
             unit_price= "3500",
             total_price= "7000",
             description= "VIP Tickets for the Party"
          }
        ,...
        ]
        """
        self.add_items(items)
        self.add_taxes(taxes)
        self.add_custom_data(custom_data)
        return self._process('checkout-invoice/create', self._prepare_data)

    def confirm(self, token=None):
        """Returns the status of the invoice

        STATUSES: pending, completed, cancelled
        """
        _token = token if token else self._response.get("token")
        return self._process('checkout-invoice/confirm/' + str(_token))

    def add_taxes(self, taxes):
        """Appends the data to the 'taxes' key in the request object

        'taxes' should be in format: [("tax_name", "tax_amount")]
        For example:
        [("Other TAX", 700), ("VAT", 5000)]
        """
        # fixme: how to resolve duplicate tax names
        _idx = len(self.taxes)  # current index to prevent overwriting
        for idx, tax in enumerate(taxes):
            tax_key = "tax_" + str(idx + _idx)
            self.taxes[tax_key] = {"name": tax[0], "amount": tax[1]}

    def add_custom_data(self, data=[]):
        """Adds the data to teh custom data sent to the server

        data format: [("phone_brand", Motorola V3"), ("model", "65456AH23")]
        """
        self.custom_data.update(dict(data))

    def add_item(self, item):
        """Updates the list of items in the current transaction"""
        _idx = len(self.items)
        self.items.update({"item_" + str(_idx + 1): item})

    def add_items(self, items):
        for item in items:
            self.add_item(item)

    def add_channel(self, channel):
        """Updates the list of payment channels in the current transaction"""
        self.channels.append(channel)

    def add_channels(self, channels):
        for channel in channels:
            self.add_channel(channel)

    @property
    def _prepare_data(self):
        """Formats the data in the current transaction for processing"""
        total_amount = self.total_amount or self.calculate_total_amt()
        self._data = {
            "invoice": {
                "items": self.__encode_items(self.items),
                "taxes": self.taxes,
                "total_amount": total_amount,
                "description": self.description,
                "channels": self.channels
            },
            "store": self.store.info,
            "custom_data": self.custom_data,
            "actions": {
                "cancel_url": self.cancel_url,
                "return_url": self.return_url,
                "callback_url": self.callback_url
            }
        }
        return self._data

    def calculate_total_amt(self, items={}):
        """Returns the total amount/cost of items in the current invoice"""
        _items = items.items() or self.items.items()
        return sum(float(x[1].total_price) for x in _items)

    def __encode_items(self, items):
        """Encodes the InvoiceItems into a JSON serializable format

        items = [('item_1',InvoiceItem(name='VIP Ticket', quantity=2,
                             unit_price='3500', total_price='7000',
                             description='VIP Tickets for party')),...]
        """
        xs = [item._asdict() for (_key, item) in items.items()]
        return list(map(lambda x: dict(zip(x.keys(), x.values())), xs))
