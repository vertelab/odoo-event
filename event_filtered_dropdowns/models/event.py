# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pytz

from odoo import _, api, fields, models
from odoo.addons.base.models.res_partner import _tz_get
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
from odoo.tools.translate import html_translate

_logger = logging.getLogger(__name__)

class EventEventType(models.Model):
    """Event Type"""
    _inherit = 'event.type'
    department_id = fields.Many2one('hr.department')
    organizer_id = fields.Many2one(
        'res.partner', string='Organizer', tracking=True,
        domain="[('type', '=', 'hr_department')]")

class EventEvent(models.Model):
    """Event"""
    _inherit = 'event.event'

    address_id = fields.Many2one(
        'res.partner', string='Venue',
        tracking=True, domain="[('type', '=', 'delivery')]")

    organizer_id = fields.Many2one(
        'res.partner', string='Organizer', tracking=True,
        domain="[('type', '=', 'hr_department')]")

    date_tz = fields.Selection(
        _tz_get, string='Timezone', required=True,
        compute='_compute_date_tz', readonly=False, store=True, default='Europe/Stockholm')

    @api.onchange("event_type_id")
    def _set_organizer_to_event_type_organizer(self):
        self.organizer_id = self.event_type_id.organizer_id
