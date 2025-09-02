import babel.dates
import re
import werkzeug

from ast import literal_eval
from collections import Counter
from werkzeug.exceptions import NotFound

from odoo import fields, http, _
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request
from odoo.osv import expression
from odoo.tools.misc import get_lang
from odoo.tools import lazy
from odoo.exceptions import UserError

from odoo.addons.website_event.controllers.main import WebsiteEventController
from odoo.addons.website_sale.controllers.main import WebsiteSale

import logging

_logger = logging.getLogger(__name__)


class CustomWebsiteEventControllerRegistration(WebsiteEventController):

    #@http.route(['''/event/<model("event.event"):event>/registration/confirm'''], type='http', auth="public", methods=['POST'], website=True)
    def dep_registration_confirm(self, event, **post):
        """ Check before creating and finalize the creation of the registrations
            that we have enough seats for all selected tickets.
            If we don't, the user is instead redirected to page to register with a
            formatted error message. """
        if not request.env['ir.http']._verify_request_recaptcha_token('website_event_registration'):
            raise UserError(_('Suspicious activity detected by Google reCaptcha.'))
        registrations_data = self._process_attendees_form(event, post)
        _logger.warning(f"{registrations_data=}")
        registration_tickets = Counter(registration['event_ticket_id'] for registration in registrations_data)
        event_tickets = request.env['event.event.ticket'].browse(list(registration_tickets.keys()))
        if any(event_ticket.seats_limited and event_ticket.seats_available < registration_tickets.get(event_ticket.id) for event_ticket in event_tickets):
            return request.redirect('/event/%s/register?registration_error_code=insufficient_seats' % event.id)
        _logger.warning(f"mar {event=}")
        attendees_sudo = self._create_attendees_from_registration_post(event, registrations_data)
        for attendee in attendees_sudo:
            attendee.state = "draft"            
        return request.redirect(('/event/%s/registration/success?' % event.id) + werkzeug.urls.url_encode({'registration_ids': ",".join([str(id) for id in attendees_sudo.ids])}))



class CustomWebsiteSaleControllerRegistration(WebsiteSale):

    #@http.route(['/shop/confirmation'], type='http', auth="public", website=True, sitemap=False)
    def dep_payment_confirmation(self, **post):
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
            attendees_in_order = request.env['event.registration'].sudo().search(
                [('sale_order_line_id', 'in', order.order_line.ids)])
            _logger.warning(f"3 did some magic {order=} {attendees_in_order=}")
            for attendee in attendees_in_order:
                attendee.state = "open"
                _logger.warning(f"4 did some magic")

            return request.render("website_sale.confirmation", {'order': order})
        else:
            return request.redirect('/shop')
