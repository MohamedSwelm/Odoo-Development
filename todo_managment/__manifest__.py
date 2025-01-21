# -*- coding: utf-8 -*-
{
    'name': "To-Do List",

    'summary': "This is an app to manage daily tasks",

    'author': "Mohammed Swelm",

    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
        'views/employee_view.xml',
        'data/sequence.xml',
        'wizards/assigned_tasks_view.xml',
        'reports/todo_report.xml',
    ],
}

