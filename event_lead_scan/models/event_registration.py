# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2022- Vertel AB (<https://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
import secrets

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

# Entropy for the per-registration scan token, in bytes before encoding.
SCAN_TOKEN_BYTES = 24


class EventRegistration(models.Model):
    """Adds the scan token and the captured leads to a registration."""
    _inherit = 'event.registration'

    scan_token = fields.Char(
        string='Scan Token',
        copy=False,
        index=True,
        readonly=True,
        help='Random token encoded in the QR code on the attendee badge. '
             'Unpredictable by design: the badge is visible to everyone '
             'in the room.',
    )
    scan_consent = fields.Boolean(
        string='Consent to Share Contact Details',
        default=False,
        help='The attendee has agreed that exhibitors may capture their '
             'contact details by scanning the badge.',
    )
    lead_ids = fields.One2many(
        comodel_name='crm.lead',
        inverse_name='event_registration_id',
        string='Captured Leads',
        readonly=True,
    )
    lead_count = fields.Integer(
        string='Leads Captured',
        compute='_compute_lead_count',
    )
    scan_token_url = fields.Char(
        string='Scan Token URL',
        compute='_compute_scan_token_url',
        help='Portal URL that displays this registration\'s scan QR code.',
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('scan_token'):
                vals['scan_token'] = self._generate_scan_token()
        return super().create(vals_list)

    @api.model
    def _generate_scan_token(self):
        """Return a scan token that is random, unique and not id-derived."""
        while True:
            token = secrets.token_urlsafe(SCAN_TOKEN_BYTES)
            if not self.sudo().search_count([('scan_token', '=', token)]):
                return token

    @api.depends('lead_ids')
    def _compute_lead_count(self):
        for registration in self:
            registration.lead_count = len(registration.lead_ids)

    @api.depends('scan_token')
    def _compute_scan_token_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param(
            'web.base.url', ''
        )
        for registration in self:
            if registration.scan_token:
                registration.scan_token_url = (
                    f'{base_url}/event_lead_scan/badge/{registration.scan_token}'
                )
            else:
                registration.scan_token_url = False

    def action_view_leads(self):
        """Open the leads captured from this registration."""
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'crm.crm_lead_all_leads'
        )
        action['domain'] = [('event_registration_id', '=', self.id)]
        action['context'] = {'default_event_registration_id': self.id}
        return action
