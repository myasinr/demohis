# -*- coding: utf-8 -*-
{
    'name': 'Odoo 13 Hospital Training Project',
    'version': '13.0.1.0.0',
    'category': 'Training/Healthcare',
    'summary': 'Complete Odoo v13 training module covering models, views, ORM, security, wizards, reports, and APIs.',
    'description': '''
Odoo 13 Hospital Training Project
=================================
A complete practical module for students. It demonstrates:
- Model and field architecture
- Relational fields: Many2one, One2many, Many2many
- Computed fields, onchange, constraints, SQL constraints
- Tree, form, search, kanban, calendar, graph, pivot views
- Menus, actions, statusbar and workflow buttons
- Security groups, ACLs, record rules, and field-level security
- Inheritance, method overriding, sequence generation
- TransientModel wizards and active_ids batch processing
- QWeb PDF report
- Chatter / mail.thread audit tracking
- Basic JSON controller for integration demo
    ''',
    'author': 'SolBizTech Training',
    'website': 'https://solbiztech.com',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'data/sequence.xml',
        'data/master_data.xml',
        'wizard/bulk_assign_doctor_wizard_views.xml',
        'views/menu.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/appointment_views.xml',
        'views/department_views.xml',
        'views/tag_views.xml',
        'views/vip_patient_views.xml',
        'views/patient_profile_views.xml',
        'views/dashboard_views.xml',
        'report/patient_report.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
