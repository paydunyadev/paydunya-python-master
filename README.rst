PAYDUNYA Python Client Library
==============================

This is a Python library for accessing the PAYDUNYA HTTP API.

Installation
------------

.. code-block:: bash

    $ sudo pip install paydunya
    $ OR git clone https://github.com/paydunya/paydunya-python
    $ cd paydunya-python; python setup.py install
    $ nosetests tests/  # run unit tests

Usage
-----

.. code-block:: python

    import paydunya
    from paydunya import InvoiceItem, Store

    # runtime configs
    PAYDUNYA_ACCESS_TOKENS = {
        'PAYDUNYA-MASTER-KEY': "Your PAYDUNYA master key",
        'PAYDUNYA-PRIVATE-KEY': "Your PAYDUNYA private key",
        'PAYDUNYA-TOKEN': "Your PAYDUNYA token"
    }
    # defaults to False
    paydunya.debug = True
    # set the access/api keys
    paydunya.api_keys = PAYDUNYA_ACCESS_TOKENS

    # Invoice
    store = Store(name='Magasin Chez Sandra')
    items = [
        InvoiceItem(
            name="Clavier DELL",
            quantity=2,
            unit_price="3000",
            total_price="6000",
            description="Best Keyboard of the 2015 year"
        ),
        InvoiceItem(
            name="Ordinateur Lenovo L440",
            quantity=1,
            unit_price="400000",
            total_price="400000",
            description="Powerful and slim"
        ),
    ]
    invoice = paydunya.Invoice(store)
    invoice.add_items(items)
    # taxes are (key,value) pairs
    invoice.add_taxes([("Other TAX", 5000), ("TVA (18%)", 700)])
    invoice.add_custom_data([
        ("first_name", "Alioune"),
        ("last_name", "Badara"),
        ("cart_id", 97628),
        ("coupon", "NOEL"),
    ])

    # you can also pass the items, taxes, custom to the `create` method
    successful, response = invoice.create()
    if successful:
        do_something_with_resp(response)

    # confirm invoice
    invoice.confirm('YOUR_INVOICE_TOKEN')


    # PSR
    opr_data = {
        'account_alias': 'EMAIL_OU_NUMERO_DU_CLIENT_PAYDUNYA',
        'description': 'Hello World',
        'total_amount': 6500
    }
    store = paydunya.Store(name='Magasin Chez Sandra')
    opr = paydunya.OPR(opr_data, store)
    # You can also pass the data to the `create` function
    successful, response = opr.create()
    if successful:
       do_something_with_response(response)
    status, _ = opr.charge({
        'token': token,
        'confirm_token': user_submitted_token
    })

    # Direct Pay
    account_alias =  "EMAIL_OU_NUMERO_DU_CLIENT_PAYDUNYA"
    amount =  6500
    # toggle debug switch to True
    direct_pay = paydunya.DirectPay(account_alias, amount)
    status, response = direct_pay.process()


License
-------
see LICENSE.txt


Contributing
------------
Issues, forks, and pull requests are welcome!


Note
----
- Some of the API calls require formal approval from PAYDUNYA
- For more information, please read the  `PAYDUNYA HTTP API`_
- Tested on Python 2.6, 2.7, and 3+.

.. _PAYDUNYA HTTP API: https://paydunya.com/developers/http

Authors
--------
PAYDUNYA <paydunya@paydunya.com>
