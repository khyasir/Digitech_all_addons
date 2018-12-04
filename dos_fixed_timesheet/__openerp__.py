# -*- coding: utf-8 -*-
{
    'name': "Dos Fixed Timesheet",

    'summary': "",

    'description': "Fields are added",

    'author': "Tax Tech",
    'website': "http://www.taxtech.com",


    # any module necessary for this one to work correctly
    'depends': ['base','account_accountant','hr_timesheet','hr','project_task_materials','project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates.xml',
    ],
}
