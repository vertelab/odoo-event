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

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class EventEvent(models.Model):
    """Exposes the event's scan sessions and captured leads."""
    _inherit = 'event.event'

    scan_session_ids = fields.One2many(
        comodel_name='event.lead.scan.session',
        inverse_name='event_id',
        string='Scan Sessions',
    )
    scan_session_count = fields.Integer(
        string='Session Count',
        compute='_compute_scan_session_count',
    )
    scan_lead_count = fields.Integer(
        string='Leads Captured',
        compute='_compute_scan_session_count',
    )

    @api.depends('scan_session_ids', 'scan_session_ids.lead_ids')
    def _compute_scan_session_count(self):
        for event in self:
            event.scan_session_count = len(event.scan_session_ids)
            event.scan_lead_count = sum(
                event.scan_session_ids.mapped('lead_count')
            )

    def action_view_scan_sessions(self):
        """Open the scan sessions of this event."""
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'event_lead_scan.action_event_lead_scan_session'
        )
        action['domain'] = [('event_id', '=', self.id)]
        action['context'] = {'default_event_id': self.id}
        return action

    def action_view_scan_leads(self):
        """Open the leads captured at this event."""
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'crm.crm_lead_all_leads'
        )
        action['domain'] = [('scan_session_id.event_id', '=', self.id)]
        return action
