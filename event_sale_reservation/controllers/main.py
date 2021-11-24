import werkzeug
from werkzeug.exceptions import NotFound

from odoo import fields, http, _
from odoo.http import request


class WebsiteEventController(http.Controller):

    @http.route(['''/event/<model("event.event"):event>/reserve/confirm'''], type='http', auth="public",
                methods=['POST'], website=True)
    def reservation_confirm(self, event, **post):
        if not event.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        partner_id = self._create_partner(post)
        order_id = self._create_sales_order_from_reservation_post(event, partner_id)

        values = {
            'attendees': partner_id,
            'event': event,
        }
        if partner_id and order_id:
            return request.render("event_sale_reservation.reservation_complete", values)
        else:
            target_url = '/event/%s/register' % str(event.id)
            return request.redirect(target_url)

    def _create_partner(self, post):
        partner_id = request.env['res.partner'].sudo().search([('email', '=', post.get('email'))], limit=1)
        if not partner_id:
            partner_id = request.env['res.partner'].sudo().create(post)
        return partner_id

    def _create_sales_order_from_reservation_post(self, event, partner_id):
        if event.event_type_id:
            product_id = request.env['product.product'].sudo().search([
                ('event_reservation_type_id', '=', event.event_type_id.id)], limit=1)
            if product_id:
                sale_order_id = request.env['sale.order'].sudo().create({
                    'partner_id': partner_id.id,
                    'partner_invoice_id': partner_id.id,
                    'partner_shipping_id': partner_id.id,
                    'order_line': [(0, 0, {
                        'product_id': product_id.id,
                        'name': event.name,
                        'product_uom_qty': 1.0,
                        'price_unit': product_id.list_price,
                        'product_uom': product_id.uom_id.id
                    })]
                })
                sale_order_id.action_confirm()
                return sale_order_id
