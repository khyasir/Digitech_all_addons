# -*- coding: utf-8 -*-
{
    'name': "dos_auto_salary",

    'summary':'Hourly & Fixed Salary Calculation',

    'description': 'Hourly & Fixed Salary Calcuation' ,

    'author': "Business Cube",
    'website': "bcube.pk",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['analytic',],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],

}