# -*- coding: utf-8 -*-
{
    'name': "Dos Entries Avg Calculation",

    'summary': "Calculation of Entries Avg",

    'description': "Fields are added Project Journal Items",

    'author': "Ehtisham Faisal",
    'website': "http://www.oxenlab.com",


    # any module necessary for this one to work correctly
    'depends': ['base','account_accountant','dos_analytic_journal'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
    'installable': True,
}
