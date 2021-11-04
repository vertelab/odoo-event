# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields


class EventEvent(models.Model):
    _name = "event.event"
    _inherit = ["event.event", "tier.validation"]
    _state_from = ["draft"]
    _state_to = ["verified"]

    state = fields.Selection([
        ('draft', 'Event Draft'),
        ('verified', 'Event Verified'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, tracking=3, default='draft')
    validated = fields.Boolean(string='Has been validated')
    

    _tier_validation_manual_config = False
