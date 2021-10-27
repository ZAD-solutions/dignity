# -*- coding: utf-8 -*-
{
    'name': 'Purchase Enhancements',
    'version': '1.0',
    'category': 'purchase',
    'author': 'Zad Solutions, Ahmed Hussein',
    'website': "http://zadsolutions.com",
    'summary': """
    Purchase Enhancements 
    """,
    'depends': [
        'base', 'purchase',
    ],
    'data': [
        'security/groups_security.xml',
        'security/ir.model.access.csv',

        'report/purchase_order_report_templates.xml',

        'views/purchase_order_view.xml',
        'views/res_config_settings_view.xml',
    ],
    'images': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
