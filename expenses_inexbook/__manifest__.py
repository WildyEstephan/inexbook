# -*- coding: utf-8 -*-
{
    'name': "Expenses INEXBOOK",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "LH Group",
    'website': "http://www.lhgroup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'hr', 'l10n_do_accounting', 'purchase', 'mail', 'project'],

    # always loaded
    'data': [
        'data/sequences.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/expenses.xml',
        'views/credit_card.xml',
        'views/time_readjustment.xml',
        'wizard/create_request.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
