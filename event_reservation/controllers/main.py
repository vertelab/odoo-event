import werkzeug
from werkzeug.exceptions import NotFound
from odoo.addons.website_event.controllers.main import WebsiteEventController

from odoo import fields, http, _
from odoo.http import request


class WebsiteEventReservationController(WebsiteEventController):

    def _process_reservation_form(self, event, form_details):
        """ Process data posted from the attendee details form.

        :param form_details: posted data from frontend registration form, like
            {'1-name': 'r', '1-email': 'r@r.com', '1-phone': '', '1-event_ticket_id': '1'}
        """
        allowed_fields = request.env['event.registration']._get_website_registration_allowed_fields()
        registration_fields = {key: v for key, v in request.env['event.registration']._fields.items() if key in allowed_fields}
        registrations = {}
        global_values = {'state': 'reservation'}
        for key, value in form_details.items():
            counter, attr_name = key.split('-', 1)
            field_name = attr_name.split('-')[0]
            if field_name not in registration_fields:
                continue
            elif isinstance(registration_fields[field_name], (fields.Many2one, fields.Integer)):
                value = int(value) or False  # 0 is considered as a void many2one aka False
            else:
                value = value

            if counter == '0':
                global_values[attr_name] = value
            else:
                registrations.setdefault(counter, dict())[attr_name] = value
        for key, value in global_values.items():
            for registration in registrations.values():
                registration[key] = value
        return list(registrations.values())

    @http.route(['''/event/<model("event.event"):event>/reserve/confirm'''], type='http', auth="public",
                methods=['POST'], website=True)
    def reservation_confirm(self, event, **post):
        if not event.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()

        registrations = self._process_reservation_form(event, post)
        if 'show_on_customer_portal' in request.env['event.registration']._fields:
            registrations[0]['show_on_customer_portal'] = True
        attendees_sudo = \
            WebsiteEventController._create_attendees_from_registration_post(
                self, event=event, registration_data=registrations
            )

        return request.render("event_reservation.reservation_complete",
            WebsiteEventController._get_registration_confirm_values(self, event, attendees_sudo))
