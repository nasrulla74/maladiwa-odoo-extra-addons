# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    'name': "POS Order Reference In Receipt 5",
    'version': '16.0.0.5',
    'category': 'Point of Sale',
    'summary': "Point of sale Order Reference In Receipt with order reference on pos receipt order reference print order reference on pos receipt reference print reference on pos receipt point of sales order reference in receipt print point of sale receipt reference print",
    'description': """

        POS Order Reference In Receipt in odoo,
        Order Reference in Receipt in odoo,
        Print Order Reference in odoo,
        Order Reference from Backend in odoo,

    """,
    'author': 'BrowseInfo',
    "price": 12,
    "currency": 'EUR',
    'website': 'https://www.browseinfo.com',
    'depends': ['base', 'point_of_sale'],
    'assets': {
        'point_of_sale.assets': [
            'bi_pos_order_reference_receipt/static/src/js/models.js',
            'bi_pos_order_reference_receipt/static/src/js/Screens/PaymentScreen/paymentScreen.js',
            'bi_pos_order_reference_receipt/static/src/js/Screens/TicketScreen/ControlButtons/ReprintReceiptButton.js',
            'bi_pos_order_reference_receipt/static/src/xml/**/*',
        ],
    },
    "license":'OPL-1',
    'installable': True,
    'auto_install': False,
    'live_test_url':'https://youtu.be/k3mwI1bzH2c',
    "images":['static/description/Banner.gif'],
}

