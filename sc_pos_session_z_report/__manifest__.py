{
    "name": "POS Session Report | POS Session Z Report | POS Session Report from front and Backend in Odoo POS",
    "description": """Using this module you can print POS Z Session Report from front and Backend in odoo POS""",
    'summary': 'Using this module you can print POS Z Session Report from front and Backend in odoo POS.',
    'category': 'Point of Sale',    
    'version': '16.3.2.1',
    'sequence': 1,
    "author" : "DOTSPRIME",
    "email": 'dotsprime@gmail.com',
    'price': 10,
    'currency': 'EUR',
    "license": 'AGPL-3',
    "depends": [
        "base",
        "point_of_sale",
    ],
    "data": [
        "report/report_pos_session.xml",
        "views/pos_session_view.xml",
    ],
    'assets': {
        'point_of_sale.assets': [
            'sc_pos_session_z_report/static/src/js/**/*',
            'sc_pos_session_z_report/static/src/xml/**/*',
        ],
    },
    'demo': [],
    'images': ['static/description/main_screenshot.jpg'],  
    "live_test_url" : "https://youtu.be/_seSqihElSg",       
    'installable': True,
    'auto_install': False,
    'application': True,
}
