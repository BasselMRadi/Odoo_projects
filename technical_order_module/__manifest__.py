{
    'name': "Technical Order Module ",
    'author': "Basel Mahmoud",
    'category': '',
    'version': '15.0.0.1.0',
    'depends': ["base", "sale",],
    'sequence': 2,
    'License':'LGPL-3.0.0.',
    'data': [
        'security/ir.model.access.csv',
        'security/groups.xml',
        'data/sequences.xml',
        'wizard/reject_reason.xml',
        'views/res_partner_views.xml',
        'views/technical_order_views.xml',
        'reports/technical_order_template_views.xml',
        'reports/ex_technical_order_template_views.xml',

    ],
    'application': True,
}

