
{
    'name': 'Sales Category',
    'version': '13',
    'author': 'Ahmed Hussein <amhussein1992@gmail.com>',

    'category': 'sale',
    'depends': ['sale', 'sale_management', 'sales_team', 'utm', 'crm', ],
    'data': [
        'data/data.xml',

        'security/groups.xml',
        'security/ir.model.access.csv',

        'views/sale_degree_view.xml',
        'views/institutions_view.xml',
        'views/disabilities_view.xml',
        'views/subscription_discontinued_reasons_view.xml',
        'views/age_groups_view.xml',
        'views/pastime_view.xml',
        'views/res_partner_view.xml',
        'views/crm_lead_view.xml',
        # 'views/sale_views.xml',

    ],
    'auto_install': False,
    'installable': True,
}
