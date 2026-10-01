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

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)

# Length of the generated tokens, in bytes of entropy before URL-safe encoding.
TOKEN_BYTES = 24


class EventLeadScanSession(models.Model):
    """A bounded scanning period owned by one exhibitor or staff member.

    The session owns its leads, its statistics and its bearer token. The
    token is what the scan web app authenticates with, so the scanner does
    not need an Odoo account.
    """
    _name = 'event.lead.scan.session'
    _description = 'Event Lead Scan Session'
    _order = 'date_start desc, id desc'

    name = fields.Char(
        string='Session Name',
        required=True,
        help='A label for this scanning session, e.g. the exhibitor name.',
    )
    event_id = fields.Many2one(
        comodel_name='event.event',
        string='Event',
        required=True,
        ondelete='cascade',
        index=True,
    )
    responsible_id = fields.Many2one(
        comodel_name='res.users',
        string='Responsible',
        required=True,
        default=lambda self: self.env.user,
        help='The person who owns the leads captured in this session.',
    )
    session_token = fields.Char(
        string='Session Token',
        required=True,
        copy=False,
        index=True,
        readonly=True,
        help='Bearer token used by the scan web app. Treated as a secret.',
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('open', 'Open'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
        copy=False,
    )
    date_start = fields.Datetime(
        string='Start Time',
        readonly=True,
        copy=False,
    )
    date_end = fields.Datetime(
        string='End Time',
        readonly=True,
        copy=False,
    )
    note = fields.Text(string='Notes')
    lead_ids = fields.One2many(
        comodel_name='crm.lead',
        inverse_name='scan_session_id',
        string='Captured Leads',
    )
    lead_count = fields.Integer(
        string='Leads',
        compute='_compute_lead_count',
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        related='event_id.company_id',
        store=True,
        readonly=True,
    )

    _sql_constraints = [
        ('session_token_uniq', 'unique(session_token)',
         'The session token must be unique.'),
    ]

    # ------------------------------------------------------------------
    # Defaults and constraints
    # ------------------------------------------------------------------
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('session_token'):
                vals['session_token'] = self._generate_token()
        return super().create(vals_list)

    @api.model
    def _generate_token(self):
        """Return a token that is random and not derived from the id."""
        while True:
            token = secrets.token_urlsafe(TOKEN_BYTES)
            if not self.sudo().search_count([('session_token', '=', token)]):
                return token

    @api.constrains('session_token')
    def _check_session_token(self):
        for session in self:
            if session.session_token and len(session.session_token) < 20:
                raise ValidationError(
                    _('The session token is too short to be considered secret.')
                )

    # ------------------------------------------------------------------
    # Computes
    # ------------------------------------------------------------------
    @api.depends('lead_ids')
    def _compute_lead_count(self):
        for session in self:
            session.lead_count = len(session.lead_ids)

    # ------------------------------------------------------------------
    # State transitions
    # ------------------------------------------------------------------
    def action_open(self):
        """Open the session for scanning."""
        for session in self:
            if session.state == 'cancelled':
                raise UserError(_('A cancelled session cannot be reopened.'))
            session.write({
                'state': 'open',
                'date_start': session.date_start or fields.Datetime.now(),
            })
        return True

    def action_done(self):
        """Close the session. Its token stops working."""
        for session in self:
            session.write({
                'state': 'done',
                'date_end': fields.Datetime.now(),
            })
        return True

    def action_cancel(self):
        """Cancel the session. Its token is rejected immediately."""
        for session in self:
            session.write({
                'state': 'cancelled',
                'date_end': fields.Datetime.now(),
            })
        return True

    def action_reset_draft(self):
        for session in self:
            session.write({'state': 'draft'})
        return True

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _is_scannable(self):
        """Return True when this session accepts scans."""
        self.ensure_one()
        return self.state == 'open'

    def action_view_leads(self):
        """Open the leads captured in this session."""
        self.ensure_one()
        action = self.env['ir.actions.act_window']._for_xml_id(
            'crm.crm_lead_all_leads'
        )
        action['domain'] = [('scan_session_id', '=', self.id)]
        action['context'] = {
            'default_scan_session_id': self.id,
            'search_default_scan_session_id': self.id,
        }
        return action
