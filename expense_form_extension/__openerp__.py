# -*- coding: utf-8 -*-
{
    'name': "expense_form_extension",

    'summary': """
        Changes in Expenses Form""",

    'description': """
        Changes in Expenses Form
    """,

    'author': "Ali",
    'website': "http://oxenlab.com",

    'category': 'Uncategorized',
    'version': '0.1',

    'depends': ['base','hr_expense','account','point_of_sale','hr_contract'],

    # always loaded
    'data': [
        'templates.xml',
        'loan.xml',
    ],
}