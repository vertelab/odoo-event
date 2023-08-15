from odoo import http
from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request

import logging
_logger = logging.getLogger(__name__)


class CustomWebsiteEventControllerRegistration(WebsiteEventController):

    @http.route(['''/event/<model("event.event"):event>/registration/confirm'''], type='http', auth="public", methods=['POST'], website=True)
    def registration_confirm(self, event, **post):
        if not event.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        registrations = self._process_attendees_form(event, post)
        attendees_sudo = self._create_attendees_from_registration_post(event, registrations)
        _logger.warning(f"1 did some magic {attendees_sudo=}")
        for attendee in attendees_sudo:
            attendee.state = "draft"
            _logger.warning(f"2 did some magic")

        return request.render("website_event.registration_complete",
            self._get_registration_confirm_values(event, attendees_sudo))

class CustomWebsiteSaleControllerRegistration(WebsiteSale):


    @http.route(['/shop/confirmation'], type='http', auth="public", website=True, sitemap=False)
    def payment_confirmation(self, **post):
        """ End of checkout process controller. Confirmation is basically seing
        the status of a sale.order. State at this point :

         - should not have any context / session info: clean them
         - take a sale.order id, because we request a sale.order and are not
           session dependant anymore
        """
        sale_order_id = request.session.get('sale_last_order_id')
        if sale_order_id:
            order = request.env['sale.order'].sudo().browse(sale_order_id)
            order.action_confirm()
            attendees_in_order = request.env['event.registration'].sudo().search([('sale_order_line_id', 'in', order.order_line.ids)])
            _logger.warning(f"3 did some magic {order=} {attendees_in_order=}")
            for attendee in attendees_in_order:
                attendee.state = "open" 
                _logger.warning(f"4 did some magic")

            return request.render("website_sale.confirmation", {'order': order})
        else:
            return request.redirect('/shop')

