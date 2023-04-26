from odoo import models, fields, api

class MottaslMessageWizard(models.TransientModel):
    _name = 'mottasl.message.wizard'
    _description = "Show Message"

    message = fields.Text('Message', required=True)

    def action_close(self):
        return {'type': 'ir.actions.act_window_close'}
