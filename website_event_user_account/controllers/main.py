# -*- coding: utf-8 -*-

from odoo import fields, http, _
from odoo.http import request
from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventControllerExtended(WebsiteEventController):

    def _create_attendees_portal_account(self, registrations_to_create, registration_id):
        for _rec, reg in zip(registrations_to_create, registration_id):
            user_id = request.env['res.users'].sudo().search([('partner_id.email', '=', _rec.get('email'))])
            if not user_id:
                user_id = request.env['res.users'].sudo().with_context(create_user=True)._create_user_from_template({
                    'name': _rec.get('name'),
                    'login': _rec.get('email'),
                    'email': _rec.get('email'),
                })
                if user_id:
                    user_id.partner_id.sudo().write({'phone': _rec.get('phone')})

                    reg.sudo().write({
                        'partner_id': user_id.partner_id.id
                    })

    def _create_attendees_from_registration_post(self, event, registration_data):
        """ Also try to set a visitor (from request) and
        a partner (if visitor linked to a user for example). Purpose is to gather
        as much informations as possible, notably to ease future communications.
        Also try to update visitor informations based on registration info. """
        visitor_sudo = request.env['website.visitor']._get_visitor_from_request(force_create=True)
        visitor_sudo._update_visitor_last_visit()
        visitor_values = {}

        registrations_to_create = []
        for registration_values in registration_data:
            registration_values['event_id'] = event.id
            if not registration_values.get('partner_id') and visitor_sudo.partner_id:
                registration_values['partner_id'] = visitor_sudo.partner_id.id
            elif not registration_values.get('partner_id'):
                registration_values['partner_id'] = request.env.user.partner_id.id

            if visitor_sudo:
                # registration may give a name to the visitor, yay
                if registration_values.get('name') and not visitor_sudo.name and not visitor_values.get('name'):
                    visitor_values['name'] = registration_values['name']
                # update registration based on visitor
                registration_values['visitor_id'] = visitor_sudo.id

            registrations_to_create.append(registration_values)

        if visitor_values:
            visitor_sudo.write(visitor_values)

        registration_id = request.env['event.registration'].sudo().create(registrations_to_create)
        if registration_id:
            self._create_attendees_portal_account(registrations_to_create, registration_id)

        return registration_id
