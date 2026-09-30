# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import werkzeug

from odoo import _, http
from odoo.http import request


class WebsiteEventController(http.Controller):
    @http.route(
        ['/event/<model("event.event"):event>/reserve/confirm'],
        type="http",
        auth="public",
        methods=["POST"],
        website=True,
    )
    def reservation_confirm(self, event, **post):
        """Reserve a seat from the public event page.

        Creates (or reuses) the partner from the posted attendee details, then
        creates and confirms a sale order for the reservation product attached
        to the event type.
        """
        if not event.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        partner_id = self._create_partner(post)
        order_id = self._create_sales_order_from_reservation_post(event, partner_id)

        if partner_id and order_id:
            return request.render(
                "website_event_sale_reservation.reservation_complete",
                {"attendees": partner_id, "event": event},
            )
        return request.redirect("/event/%s/register" % str(event.id))

    def _create_partner(self, post):
        partner_id = (
            request.env["res.partner"]
            .sudo()
            .search([("email", "=", post.get("email"))], limit=1)
        )
        if not partner_id:
            partner_id = request.env["res.partner"].sudo().create(post)
        return partner_id

    def _create_sales_order_from_reservation_post(self, event, partner_id):
        if not event.event_type_id:
            return False
        product_id = (
            request.env["product.product"]
            .sudo()
            .search(
                [
                    ("event_reservation_ok", "=", True),
                    ("event_reservation_type_id", "=", event.event_type_id.id),
                ],
                limit=1,
            )
        )
        if not product_id:
            return False
        sale_order_id = (
            request.env["sale.order"]
            .sudo()
            .create(
                {
                    "partner_id": partner_id.id,
                    "partner_invoice_id": partner_id.id,
                    "partner_shipping_id": partner_id.id,
                    "order_line": [
                        (
                            0,
                            0,
                            {
                                "product_id": product_id.id,
                                "name": event.name,
                                "product_uom_qty": 1.0,
                                "price_unit": product_id.list_price,
                                "product_uom": product_id.uom_id.id,
                            },
                        )
                    ],
                }
            )
        )
        sale_order_id.action_confirm()
        return sale_order_id
