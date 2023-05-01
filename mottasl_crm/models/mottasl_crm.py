# -*- coding: utf-8 -*-
import requests

from odoo import models


class MottaslCrm(models.Model):
    _inherit = 'crm.lead'

    def send_wa_message(self, record=None):
        # get required mottasl config parameters
        c = self._get_config_params()

        # validate config parameters
        is_missing_required_config = not c['mottasl_api_key'] or not c[
            'mottasl_template_id'] or not c['mottasl_template_lang'] or not c['mottasl_template_type']
        if is_missing_required_config:
            return self._open_popup('Some Mottasl cofigurations are missing. Please complete them in settings', 'Error')
        # validate phone number
        phone_number = record.phone if record else self.phone
        if not phone_number:
            return self._open_popup('This lead does not have phone number', 'Error')
        is_phone_e164_format = str(phone_number).startswith('+')
        if not is_phone_e164_format:
            return self._open_popup('Phone number of lead should be in E.164 format with leading +', 'Error')

        # send template message then check failure
        response = self._send_template_message(phone_number, c)
        if response.status_code != 200 and response.status_code != 202:
            error_message = response.json()['message']
            return self._open_popup(f'Error happended while sending message, Error description: {error_message}.', 'Error')

        # message sent with no error, make note and alert success
        self._log_wa_message(record, response.json()['messageId'], c)
        return self._open_popup('Message sent successfully.', 'Success')

    def send_mulitple_wa_messages(self):
        selected_ids = self.env.context.get('active_ids', [])
        selected_records = self.env['crm.lead'].browse(selected_ids)

        messages_succeeded = 0
        for record in selected_records:
            result = self.send_wa_message(record)
            if result['name'] == 'Success':
                messages_succeeded += 1

        return self._open_popup(f'{messages_succeeded}/{len(selected_ids)} messages succeeded', 'Done')

    def _get_config_params(self):
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

        return {
            'mottasl_api_key': mottasl_api_key,
            'mottasl_template_id': mottasl_template_id,
            'mottasl_template_lang': mottasl_template_lang,
            'mottasl_template_type': mottasl_template_type,
            'mottasl_template_args': mottasl_template_args,
        }

    def _send_template_message(self, phone_number, config_params):
        url = "https://chat.zoko.io/v2/message"
        payload = {
            "channel": "whatsapp",
            "recipient": phone_number,
            "templateId": config_params['mottasl_template_id'],
            "type": config_params['mottasl_template_type'],
            "templateLanguage": config_params['mottasl_template_lang'],
            "templateArgs": str(config_params['mottasl_template_args']).split(',')
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "apikey": config_params['mottasl_api_key'],
        }

        response = requests.post(url, json=payload, headers=headers)
        return response

    def _open_popup(self, popup_message, title='Message'):
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

    def _get_mottasl_message_body(self, message_id, mottasl_api_key):
        # 34546bb0-e793-11ed-8b51-4b2e72444814
        url = f"https://chat.zoko.io/v2/message/{message_id}"

        headers = {
            "accept": "application/json",
            "apikey": mottasl_api_key
        }

        response = requests.get(url, headers=headers)
        return response.json()['text']

    def _log_note(self, record, note):
        r = record or self
        r.message_post(body=note,
                       message_type='comment', subtype_xmlid='mail.mt_note', partner_ids=[], attachment_ids=[])

    def _log_wa_message(self, record, message_id, config_params):
        message_body = self._get_mottasl_message_body(
            message_id, config_params['mottasl_api_key'])
        success_note = """<b>WA Template Sent</b> <br/><br/>
        Temp ID: {} <br/>
        Temp Lang: {} <br/>
        Message: {}<br/>""".format(config_params['mottasl_template_id'], config_params['mottasl_template_lang'], message_body)
        self._log_note(record, success_note)
