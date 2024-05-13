import babel.dates
import re
import werkzeug

from ast import literal_eval
from werkzeug.datastructures import OrderedMultiDict
from werkzeug.exceptions import NotFound

from odoo import fields, http, _
from odoo.addons.website.controllers.main import QueryURL
from odoo.http import request
from odoo.osv import expression
from odoo.tools.misc import get_lang
from odoo.tools import lazy
from odoo.exceptions import UserError

from odoo.addons.website_event.controllers.main import WebsiteEventController


class WebsiteEventWaitlistController(WebsiteEventController):
    # ------------------------------------------------------------
    # EVENT LIST
    # ------------------------------------------------------------

    def _get_events_search_options(self, **post):
        return {
            'displayDescription': False,
            'displayDetail': False,
            'displayExtraDetail': False,
            'displayExtraLink': False,
            'displayImage': False,
            'allowFuzzy': not post.get('noFuzzy'),
            'date': post.get('date'),
            'tags': post.get('tags'),
            'type': post.get('type'),
            'country': post.get('country'),
        }

    @http.route(['/event-type', '/event-type/page/<int:page>', '/event-types', '/event-types/page/<int:page>'],
                type='http', auth="public", website=True)
    def event_types(self, page=1, **searches):
        Event = request.env['event.type'].sudo()

        searches.setdefault('search', '')
        searches.setdefault('tags', '')

        website = request.website

        step = 12  # Number of events per page

        options = self._get_events_search_options(**searches)
        order = 'create_date'
        if searches.get('date', 'upcoming') == 'old':
            order = 'create_date desc'
        order = 'is_published desc, ' + order
        search = searches.get('search')
        event_count, details, fuzzy_search_term = website._search_with_fuzzy("event_types", search,
                                                                             limit=page * step, order=order,
                                                                             options=options)
        event_details = details[0]
        events = event_details.get('results', Event)
        events = events[(page - 1) * step:page * step]

        # count by domains without self search
        domain_search = [('name', 'ilike', fuzzy_search_term or searches['search'])] if searches['search'] else []

        # no_date_domain = event_details['no_date_domain']
        # dates = event_details['dates']
        # for date in dates:
        #     if date[0] not in ['all', 'old']:
        #         date[3] = Event.search_count(expression.AND(no_date_domain) + domain_search + date[2])

        # no_country_domain = event_details['no_country_domain']
        # countries = Event.read_group(expression.AND(no_country_domain) + domain_search, ["id", "country_id"],
        #                              groupby="country_id", orderby="country_id")
        # countries.insert(0, {
        #     'country_id_count': sum([int(country['country_id_count']) for country in countries]),
        #     'country_id': ("all", _("All Countries"))
        # })

        search_tags = event_details['search_tags']
        # current_date = event_details['current_date']
        current_type = None
        current_country = None

        # if searches["type"] != 'all':
        #     current_type = SudoEventType.browse(int(searches['type']))
        #
        # if searches["country"] != 'all' and searches["country"] != 'online':
        #     current_country = request.env['res.country'].browse(int(searches['country']))

        pager = website.pager(
            url="/event-type",
            url_args=searches,
            total=event_count,
            page=page,
            step=step,
            scope=5)

        keep = QueryURL('/event-type', **{
            key: value for key, value in searches.items() if (
                    key == 'search' or
                    (value != 'upcoming' if key == 'date' else value != 'all'))
        })

        searches['search'] = fuzzy_search_term or search

        values = {
            # 'current_date': current_date,
            'current_country': current_country,
            'current_type': current_type,
            'event_type_ids': events.sudo(),  # event_ids used in website_event_track so we keep name as it is
            'categories': request.env['event.tag.category'].search([
                ('is_published', '=', True), '|', ('website_id', '=', website.id), ('website_id', '=', False)
            ]),
            # 'countries': countries,
            'pager': pager,
            'searches': searches,
            'search_tags': search_tags,
            'keep': keep,
            'search_count': event_count,
            'original_search': fuzzy_search_term and search,
            'website': website
        }
        return request.render("event_waitlist_website.index_event_types", values)

    @http.route(['''/event-type/<model("event.type"):event_type>'''], type='http', auth="public", website=True,
                sitemap=False)
    def event_type_register(self, event_type, **post):
        values = self._prepare_event_type_register_values(event_type, **post)
        return request.render("event_waitlist_website.event_type_description_full", values)

    def _prepare_event_type_register_values(self, event_type, **post):
        """Return the require values to render the template."""
        return {
            'event_type': event_type.sudo(),
            'main_object': event_type.sudo(),
            'range': range,
        }

    @http.route(['/event-type/<model("event.type"):event_type>/waiting-list-registration/new'], type='http',
                auth="public", methods=['POST'], website=True)
    def waiting_list_registration_new(self, event_type, **post):
        """ Check before creating and finalize the creation of the registrations
                    that we have enough seats for all selected tickets.
                    If we don't, the user is instead redirected to page to register with a
                    formatted error message. """
        registrations_data = self._process_waiting_list_form(event_type, post)
        print("registrations_data", registrations_data)
        # event_ticket_ids = {registration['event_ticket_id'] for registration in registrations_data}
        # event_tickets = request.env['event.event.ticket'].browse(event_ticket_ids)
        # if any(event_ticket.seats_limited and event_ticket.seats_available < len(registrations_data) for event_ticket in
        #        event_tickets):
        #     return request.redirect('/event/%s/register?registration_error_code=insufficient_seats' % event_type.id)
        waiting_list_sudo = self._create_waiting_list_from_post(event_type, registrations_data)

        return request.redirect(('/event-type/%s/waitlist/success?' % event_type.id) + werkzeug.urls.url_encode(
            {'waiting_list_ids': ",".join([str(id) for id in waiting_list_sudo.ids])}))

    @http.route(['/event-type/<model("event.type"):event_type>/waitlist/success'], type='http', auth="public",
                methods=['GET'], website=True, sitemap=False)
    def event_waitlist_registration_success(self, event_type, waiting_list_ids):
        # fetch the related registrations, make sure they belong to the correct visitor / event pair
        visitor = request.env['website.visitor']._get_visitor_from_request()
        if not visitor:
            raise NotFound()
        waiting_list_sudo = request.env['event.waiting.list'].sudo().search([
            ('id', 'in', [str(waiting_list_id) for waiting_list_id in waiting_list_ids.split(',')]),
            ('event_type_id', '=', event_type.id),
            ('visitor_id', '=', visitor.id),
        ])
        if not waiting_list_sudo:
            raise NotFound()
        vals = {'waiting_list_ids': waiting_list_sudo, 'event_type': event_type}
        return request.render("event_waitlist_website.registration_waitlist_complete", vals)

    def _process_waiting_list_form(self, event_type, form_details):
        """ Process data posted from the attendee details form.
        Extracts question answers:
        - For both questions asked 'once_per_order' and questions asked to every attendee
        - For questions of type 'simple_choice', extracting the suggested answer id
        - For questions of type 'text_box', extracting the text answer of the attendee.

        :param form_details: posted data from frontend registration form, like
            {'1-name': 'r', '1-email': 'r@r.com', '1-phone': '', '1-event_ticket_id': '1'}
        """
        allowed_fields = request.env['event.waiting.list']._get_website_registration_allowed_fields()
        registration_fields = {
            key: v for key, v in request.env['event.waiting.list']._fields.items() if key in allowed_fields
        }

        registrations = {}
        general_answer_ids = []
        general_identification_answers = {}
        # as we may have several questions populating the same field (e.g: the phone)
        # we use this to hold the fields that have already been handled
        # goal is to use the answer to the first question of every 'type' (aka name / phone / email / company name)
        already_handled_fields_data = {}
        for key, value in form_details.items():
            if not value:
                continue

            key_values = key.split('-')

            # Special case for handling event_ticket_id data that holds only 2 values
            if len(key_values) == 2:
                registration_index, field_name = key_values
                if field_name not in registration_fields:
                    continue
                registrations.setdefault(registration_index, dict())[field_name] = value or False
                continue

            registration_index, question_type, question_id = key_values

            if question_type in ('name', 'email', 'phone', 'company_name') \
                    and question_type not in already_handled_fields_data.get(registration_index, []):
                if question_type not in registration_fields:
                    continue

                field_name = question_type
                already_handled_fields_data.setdefault(registration_index, list()).append(field_name)

                if not int(registration_index):
                    general_identification_answers[field_name] = value
                else:
                    registrations.setdefault(registration_index, dict())[field_name] = value

        if general_identification_answers:
            for registration in registrations.values():
                registration.update(general_identification_answers)

        return list(registrations.values())

    def _create_waiting_list_from_post(self, event_type, registration_data):
        """ Also try to set a visitor (from request) and
        a partner (if visitor linked to a user for example). Purpose is to gather
        as much information as possible, notably to ease future communications.
        Also try to update visitor information based on registration info. """
        visitor_sudo = request.env['website.visitor']._get_visitor_from_request(force_create=True)

        registrations_to_create = []
        for registration_values in registration_data:
            registration_values['event_type_id'] = event_type.id
            if not registration_values.get('partner_id') and visitor_sudo.partner_id:
                registration_values['partner_id'] = visitor_sudo.partner_id.id
            elif not registration_values.get('partner_id'):
                registration_values[
                    'partner_id'] = False if request.env.user._is_public() else request.env.user.partner_id.id

            # update registration based on visitor
            registration_values['visitor_id'] = visitor_sudo.id

            registrations_to_create.append(registration_values)

        return request.env['event.waiting.list'].sudo().create(registrations_to_create)
