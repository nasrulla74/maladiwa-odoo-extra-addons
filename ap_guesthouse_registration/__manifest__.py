
{
    'name': 'Hotel Checkin/Registration 1.7.6',
    'version': '1.7.6',
    'summary': 'Guest House Management Application',
    'description': """
                        Adding new feauture: verison : 1.7.1
                        
                        The module helps you to manage rooms,amenities,services,restaurants.
                        End Users can book rooms and reserve foods from hotel restaurant.""",
    'author': 'Appeul Services',
    'company': 'Appeul',
    'maintainer': 'Appeul Services',
    'category': 'Sales',
    'website': 'https://www.appeul.com',
    'sequence':"-1110",
    'depends': ['base', 'wt_hotel_reservation', 'sale', 'point_of_sale', 'web', 'board'],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/wizard_guest_extend.xml',
        'views/gh_register_view.xml',
        'views/menus.xml',
        'views/hotel_today_arrival.xml',
        'views/fo_dashboard.xml',
        'views/hotel_ex_activities.xml',
        'views/hotel_complaints.xml',
        'views/hotel_departures.xml',
        'report/ap_gh_reg_card.xml',
        'report/report.xml',
    ],

    'installable': True,
    'application': True,

    'assets': {
            'web.assets_backend': [
                'ap_guesthouse_registration/static/src/components/**/*.js',
                'ap_guesthouse_registration/static/src/components/**/*.xml',
                'ap_guesthouse_registration/static/src/components/**/*.scss',
                # 'ap_guesthouse_registration/static/src/components/*/*.js',
                # 'ap_guesthouse_registration/static/src/components/*/*.xml',
                # 'ap_guesthouse_registration/static/src/components/*/*.scss',
            ],
            'point_of_sale.assets': [
                'ap_guesthouse_registration/static/src/pos/**/*.js',
                'ap_guesthouse_registration/static/src/pos/**/*.xml',
                'ap_guesthouse_registration/static/src/pos/**/*.scss',
            ]
        },


    'license': 'LGPL-3',

}
