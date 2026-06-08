# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import html_translate

import logging

_logger = logging.getLogger(__name__)

# TODO: Extend tier_definition in https://github.com/OCA/server-ux/blob/14.0/base_tier_validation/models/tier_definition.py with multiple user alternative.
# Includes implementing a system variable to define the required amount of reviwers.


class EventType(models.Model):
    _name = "event.type"
    _description = 'Event Template'
    _inherit = ["event.type", "tier.validation"]
    _state_from = ["draft"]
    _state_to = ["reviewed", "approved"]

    state = fields.Selection([
        ('draft', 'Event Template Draft'),
        ('reviewed', 'Event Template Reviewed')
    ], string='Status', readonly=True, store=True, index=True, default='draft', copy=False)

    _tier_validation_manual_config = False

    @api.model
    def _valid_field_parameter(self, field, name):
        return name == 'tracking' or super()._valid_field_parameter(field, name)

    def confirm_state(self):
        self.state = 'reviewed'


    def draft_state(self):
        self.restart_validation()
        self.state = 'draft'
