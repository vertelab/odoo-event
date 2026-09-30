# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    event_registration_count = fields.Integer(
        compute="_compute_event_registration_count",
        string=_("Event registrations"),
        help=_("Indicates how many event registrations are linked to this order."),
    )

    @api.depends("order_line.event_registration_ids")
    def _compute_event_registration_count(self):
        """Get registrations per SO."""
        for one in self:
            one.event_registration_count = len(
                one.mapped("order_line.event_registration_ids")
            )

    def action_open_event_registrations(self):
        """Redirect user to event registrations related to this SO."""
        return {
            "domain": [("sale_order_id", "in", self.ids)],
            "name": _("Attendees"),
            "res_model": "event.registration",
            "type": "ir.actions.act_window",
            "view_mode": "list,form,calendar,graph",
            "view_type": "form",
        }
