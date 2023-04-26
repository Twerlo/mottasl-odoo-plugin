# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Mottasl WA for CRM',
    'version': '1.0',
    'category': 'Sales/CRM',
    'summary': 'Use Mottasl WA messaging in your CRM application',
    'depends': ['crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/crm_lead_views.xml',
        'wizard/message_wizard.xml',
        
        'views/res_config_seetings_view.xml',
    ],
    'installable': True,
    'application': True,
    'price': 49.99,
    'currency': 'USD',
    'license': 'LGPL-3',
}
