# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http, _
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager
from odoo.exceptions import AccessError, MissingError
from collections import OrderedDict
from odoo.http import request
import werkzeug

import logging
_logger = logging.getLogger(__name__)

class PortalEvent(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        partner = request.env.user.partner_id

        EventAttendee = request.env['event.registration'].sudo()
        if 'event_count' in counters:
            event_count = EventAttendee.search_count(self._get_event_domain()) \
                if EventAttendee.check_access_rights('read', raise_exception=False) else 0
            values['event_count'] = event_count
        return values

    def _get_event_domain(self):
        partner = request.env.user.partner_id
        # return [('email', '=', partner.email)]
        return [('partner_id', '=', partner.id)]

    @http.route(['/my/events', '/my/events/page/<int:page>'], type='http', auth="user", website=True)
    def portal_my_events(self, page=1, create_date=None, date_closed=None, sortby=None, filterby=None, **kw):
        values = self._prepare_portal_layout_values()
        EventAttendee = request.env['event.registration'].sudo()

        domain = self._get_event_domain()

        searchbar_sortings = {
            'create_date': {'label': _('Date'), 'order': 'create_date desc'},
            'date_closed': {'label': _('Due Date'), 'order': 'date_closed desc'},
            'name': {'label': _('Event'), 'order': 'name desc'},
            'state': {'label': _('Status'), 'order': 'state'},
        }
        # default sort by order
        if not sortby:
            sortby = 'create_date'
        order = searchbar_sortings[sortby]['order']
        active_stage_ids = request.env['event.stage'].search([('name','not ilike','Cancelled'),('name','not ilike','Ended')]).ids
        _logger.error(f"{active_stage_ids=}"*50)
        active_event_ids = request.env['event.event'].search([('stage_id','in',active_stage_ids)]).ids
        _logger.error(f"{active_event_ids=}"*50)
        searchbar_filters = {
            'all': {'label': _('All'), 'domain': []},
            'confirmed': {'label': _('Confirmed'), 'domain': [('state', '=', 'open')]},
            'cancelled': {'label': _('Cancelled'), 'domain': [('state', '=', 'cancel')]},
            'ongoing': {'label': _('Ongoing'), 'domain': [('event_id', 'in', active_event_ids)]},
        }
        # default filter by value
        if not filterby:
            filterby = 'all'
        domain += searchbar_filters[filterby]['domain']

        if create_date and date_closed:
            domain += [('date_open', '>', create_date), ('date_closed', '<=', date_closed)]

        # count for pager
        event_count = EventAttendee.search_count(domain)
        # pager
        pager = portal_pager(
            url="/my/events",
            url_args={'create_date': create_date, 'date_closed': date_closed, 'sortby': sortby},
            total=event_count,
            page=page,
            step=self._items_per_page
        )
        # content according to pager and archive selected
        events = EventAttendee.search(domain, order=order, limit=self._items_per_page, offset=pager['offset'])
        
        request.session['my_events_history'] = events.ids[:100]

        values.update({
            'date': create_date,
            'events': events,
            'page_name': 'events',
            'pager': pager,
            'default_url': '/my/events',
            'searchbar_sortings': searchbar_sortings,
            'sortby': sortby,
            'searchbar_filters': OrderedDict(sorted(searchbar_filters.items())),
            'filterby': filterby,
        })
        return request.render("website_event_portal.portal_my_events", values)

    def _event_get_page_view_values(self, event_registration, access_token, **kwargs):
        values = {
            'page_name': 'event_registration',
            'event_registration': event_registration,
        }
        return self._get_page_view_values(
            event_registration, access_token, values, 'my_event_reservation_history', False, **kwargs)

    @http.route(['/event/<int:event_registration_id>',
                 '/event/<int:event_registration_id>/un-reserve'], type='http', auth="user", website=True)
    def portal_my_event_reservations(self, event_registration_id=None, access_token=None, **kw):
        try:
            event_reg_sudo = self._document_check_access('event.registration', event_registration_id, access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')
        if kw.get('action') == 'unreserve':
            event_reg_sudo.action_cancel()

        values = self._event_get_page_view_values(event_reg_sudo, access_token, **kw)
        return request.render("website_event_portal.event_my_event_registration", values)

