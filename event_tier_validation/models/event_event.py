# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)

# TODO: Extend tier_definition in https://github.com/OCA/server-ux/blob/14.0/base_tier_validation/models/tier_definition.py with multiple user alternative.
# Includes implementing a system variable to define the required amount of reviwers.


class EventEvent(models.Model):
    _name = "event.event"
    _inherit = ["event.event", "tier.validation"]
    _state_from = ["draft"]
    _state_to = ["reviewed", "approved"]

    state = fields.Selection([
        ('draft', 'Event Draft'),
        ('reviewed', 'Event Reviewed')
    ], string='Status', readonly=True, store=True, index=True, tracking=3, default='draft', copy=False)

    _tier_validation_manual_config = False

    @api.constrains("state", "website_published", "is_published")  
    def _check_state(self):
        for record in self:
            if record.review_ids:
                current_review = record.review_ids.sorted(
                    key=lambda r: r.create_date)[0]
                reviewers = len(current_review.done_by)
                if reviewers:
                    record.state = 'reviewed'
                else:
                    raise UserError(
                        _("This event has not been reviewed, please ask your reviewers to take a look."))
            elif self.is_published and not record.validated:
                raise UserError(
                    _("This event has not been reviewed yet, please start a review process by pressing 'Request Validation' button."))