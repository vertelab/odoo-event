# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # OCA/event_sale_reservation marks reservation products through the core
    # ``service_tracking`` field (selection value ``event_reservation``).
    # ``event_reservation_ok`` is a read-only convenience alias so that website
    # templates, domains and the booking controller can express intent without
    # hard-coding the selection value everywhere.
    event_reservation_ok = fields.Boolean(
        string="Is an event reservation",
        compute="_compute_event_reservation_ok",
        search="_search_event_reservation_ok",
        help="If checked, this product enables selling event reservations "
        "even before an event of the specified type has been scheduled.",
    )

    @api.depends("service_tracking")
    def _compute_event_reservation_ok(self):
        for one in self:
            one.event_reservation_ok = (
                one.service_tracking == "event_reservation"
            )

    def _search_event_reservation_ok(self, operator, value):
        """Search ``event_reservation_ok`` through ``service_tracking``.

        Supports the ``=``/``!=`` operators with a boolean value, which is all
        the domains in this module use.
        """
        if operator not in ("=", "!="):
            raise NotImplementedError(
                _("Unsupported operator %(operator)s for event_reservation_ok.")
                % {"operator": operator}
            )
        if operator == "!=":
            value = not value
        if value:
            return [("service_tracking", "=", "event_reservation")]
        return [("service_tracking", "!=", "event_reservation")]
