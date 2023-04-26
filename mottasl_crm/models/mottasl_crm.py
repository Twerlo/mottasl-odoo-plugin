# -*- coding: utf-8 -*-
import requests

from odoo import models


class MottaslCrm(models.Model):
    _inherit = 'crm.lead'

    # mottasl_api_key = fields.Char()
    # tag_ids = fields.Many2many(
    #     'crm.lead', 'crm_lead_mottasl_rel',
    #     'mottasl_id', 'lead_id',
    #     string='Tags')

    def send_wa_message(self):
        # get required mottasl config parameters
        mottasl_api_key = self.env['ir.config_parameter'].sudo(
        ).get_param('mottasl_crm.mottasl_api_key', False)
        mottasl_template_id = self.env['ir.config_parameter'].sudo(
        ).get_param('mottasl_crm.mottasl_template_id', False)
        mottasl_template_lang = self.env['ir.config_parameter'].sudo(
        ).get_param('mottasl_crm.mottasl_template_lang', False)
        mottasl_template_type = self.env['ir.config_parameter'].sudo(
        ).get_param('mottasl_crm.mottasl_template_type', False)
        mottasl_template_args = self.env['ir.config_parameter'].sudo(
        ).get_param('mottasl_crm.mottasl_template_args', False)

        is_missing_required_config = not mottasl_api_key or not mottasl_template_id or not mottasl_template_lang or not mottasl_template_type

        if is_missing_required_config:
            return self.open_popup('Some Mottasl cofigurations are missing. Please complete them in settings', 'Error')

        self.ensure_one()
        if not self.phone:
            return self.open_popup('This lead does not have phone number', 'Error')

        is_phone_e164_format = str(self.phone).startswith('+')

        if not is_phone_e164_format:
            return self.open_popup('Phone number of lead should be in E.164 format with leading +', 'Error')

        url = "https://chat.zoko.io/v2/message"
        payload = {
            "channel": "whatsapp",
            "recipient": self.phone,
            "templateId": mottasl_template_id,
            "type": mottasl_template_type,
            "templateLanguage": mottasl_template_lang,
            "templateArgs": str(mottasl_template_args).split(',')
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "apikey": mottasl_api_key,
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200 and response.status_code != 202:
            error_message = response.json()['message']
            return self.open_popup(f'Error happended while sending message, Error description: {error_message}.', 'Error')

        # Message sent with no error
        return self.open_popup('Message sent successfully.', 'Success')

    def open_popup(self, popup_message, title='Message'):
        message_id = self.env['mottasl.message.wizard'].create(
            {'message': popup_message})
        return {
            'name': title,
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mottasl.message.wizard',
            'res_id': message_id.id,
            'target': 'new'
        }
