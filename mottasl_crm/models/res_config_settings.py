from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    mottasl_api_key = fields.Char(string='Mottasl API Key', config_parameter='mottasl_crm.mottasl_api_key',
                                  help='Mottasl API Key related to your mottasl account', size=36, required=True)
    mottasl_template_id = fields.Char(string='Mottasl Template ID', config_parameter='mottasl_crm.mottasl_template_id',
                                      help='ID of the template that will be sent to chosen leads', required=True)
    mottasl_template_lang = fields.Char(string='Mottasl Template Language', config_parameter='mottasl_crm.mottasl_template_lang',
                                        help='Langague of the template that will be sent to chosen leads (ar|en)', size=2, required=True)

    mottasl_template_type = fields.Char(string='Mottasl Template Type', config_parameter='mottasl_crm.mottasl_template_type',
                                        help='Type of the template that will be sent to chosen leads (template|buttonTemplate|richTemplate)', required=True)
    mottasl_template_args = fields.Char(string='Mottasl Template Args', config_parameter='mottasl_crm.mottasl_template_args',
                                        help='Args of the template that will be sent to chosen leads (Separated by commas ",")')
