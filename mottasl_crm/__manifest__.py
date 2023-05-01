# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mottasl WA for CRM',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Use Mottasl WA messaging in your CRM application',
    'depends': ['crm'],
    'author': "Twerlo",
    'images': ['images/main_screenshot.png'],
    'data': [
        'views/crm_lead_views.xml',
        'views/crm_case_tree_view_oppor.xml',
        'views/res_config_settings_view.xml',

        'security/ir.model.access.csv',

        'wizard/message_wizard.xml',
    ],
    'installable': True,
    'application': True,
    'price': 0.0,
    'currency': 'USD',
    'license': 'LGPL-3',
}
