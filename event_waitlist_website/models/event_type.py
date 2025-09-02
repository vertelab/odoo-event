from ast import literal_eval
from dateutil.relativedelta import relativedelta
import json
import werkzeug.urls

from pytz import utc, timezone

from odoo import models, fields, api, _
#from odoo.addons.http_routing.models.ir_http import slug
from odoo.http import request
from odoo.tools.translate import html_translate
from odoo.addons.base.models.res_partner import _tz_get
from odoo.exceptions import ValidationError
from odoo.osv import expression
from odoo.tools.misc import get_lang, format_date

GOOGLE_CALENDAR_URL = 'https://www.google.com/calendar/render?'


class EventType(models.Model):
    _name = 'event.type'
    _inherit = [
        'event.type',
        'website.seo.metadata',
        'website.published.multi.mixin',
        'website.cover_properties.mixin',
        'website.searchable.mixin',
    ]

    @api.depends('name')
    def _compute_waiting_list_count(self):
        for rec in self:
            rec.waiting_list_count = self.env['event.waiting.list'].search_count([('event_type_id', '=', rec.id)])

    waiting_list_count = fields.Integer(string="Waitlisting Count", compute=_compute_waiting_list_count)

    def action_view_waitlist(self):
        event_waitlist_list_view = self.env.ref('event_waitlist_website.view_event_waiting_list')
        return {
            'name': _('Waiting List'),
            'domain': [('event_type_id', '=', self.id)],
            'res_model': 'event.waiting.list',
            'type': 'ir.actions.act_window',
            'view_id': event_waitlist_list_view.id,
            'views': [(event_waitlist_list_view.id, 'list'), (False, 'form')],
            'view_mode': 'list,form',
            'context': "{'default_event_type_id_id': %d}" % self.id
        }

    date_tz = fields.Selection(
        _tz_get, string='Timezone', required=True,
        compute='_compute_date_tz', precompute=True, readonly=False, store=True)
    company_id = fields.Many2one(
        'res.company', string='Company', change_default=True,
        default=lambda self: self.env.company,
        required=False)

    event_ids = fields.One2many('event.event', 'event_type_id', string="Events")

    open_waiting_list = fields.Boolean(string="Accept Waiting List")

    @api.depends('default_timezone')
    def _compute_date_tz(self):
        for event in self:
            if event.default_timezone:
                event.date_tz = event.default_timezone
            if not event.date_tz:
                event.date_tz = self.env.user.tz or 'UTC'

    def _default_description(self):
        # avoid template branding with rendering_bundle=True
        return self.env['ir.ui.view'].with_context(rendering_bundle=True) \
            ._render_template('event.event_default_descripton')

    description = fields.Html(string='Description', translate=html_translate, sanitize_attributes=False,
                              sanitize_form=False, default=_default_description)

    subtitle = fields.Char('Event Subtitle', translate=True)

    address_id = fields.Many2one(
        'res.partner', string='Venue', default=lambda self: self.env.company.partner_id.id,
        check_company=True,
        tracking=True
    )

    def _default_cover_properties(self):
        res = super()._default_cover_properties()
        res['opacity'] = '0.4'
        return res

    # website
    website_published = fields.Boolean(tracking=True)
    menu_id = fields.Many2one('website.menu', 'Event Menu', copy=False)
    address_name = fields.Char(related='address_id.name')

    organizer_id = fields.Many2one(
        'res.partner', string='Organizer', tracking=True,
        default=lambda self: self.env.company.partner_id,
        check_company=True)

    def _set_tz_context(self):
        self.ensure_one()
        return self.with_context(tz=self.date_tz or 'UTC')

    def _google_map_link(self, zoom=8):
        self.ensure_one()
        if self.address_id:
            return self.sudo().address_id.google_map_link(zoom=zoom)
        return None

    def google_map_link(self, zoom=8):
        """ Temporary method for stable """
        return self._google_map_link(zoom=zoom)

    @api.depends('name')
    def _compute_website_url(self):
        #from odoo.http import request
        slug = request.env['ir.http']._slug
        super(EventType, self)._compute_website_url()
        for event_type in self:
            if event_type.id:
                event_type.website_url = '/event-type/%s' % slug(event_type)

    @api.model
    def _search_get_detail(self, website, order, options):
        with_description = options['displayDescription']
        with_date = options['displayDetail']
        date = options.get('date', 'all')
        country = options.get('country')
        tags = options.get('tags')

        domain = [website.website_domain()]

        search_tags = self.env['event.tag']
        if tags:
            try:
                tag_ids = literal_eval(tags)
            except SyntaxError:
                pass
            else:
                # perform a search to filter on existing / valid tags implicitely + apply rules on color
                search_tags = self.env['event.tag'].search([('id', 'in', tag_ids)])

            # Example: You filter on age: 10-12 and activity: football.
            # Doing it this way allows to only get events who are tagged "age: 10-12" AND "activity: football".
            # Add another tag "age: 12-15" to the search and it would fetch the ones who are tagged:
            # ("age: 10-12" OR "age: 12-15") AND "activity: football
            for tags in search_tags.grouped('category_id').values():
                domain.append([('tag_ids', 'in', tags.ids)])

        no_country_domain = domain.copy()
        if country:
            if country == 'online':
                domain.append([("country_id", "=", False)])
            elif country != 'all':
                domain.append(['|', ("country_id", "=", int(country)), ("country_id", "=", False)])

        no_date_domain = domain.copy()
        current_date = None

        search_fields = ['name']
        fetch_fields = ['name', 'website_url', 'address_name']
        mapping = {
            'name': {'name': 'name', 'type': 'text', 'match': True},
            'website_url': {'name': 'website_url', 'type': 'text', 'truncate': False},
            'address_name': {'name': 'address_name', 'type': 'text', 'match': True},
        }
        if with_description:
            search_fields.append('subtitle')
            fetch_fields.append('subtitle')
            mapping['description'] = {'name': 'subtitle', 'type': 'text', 'match': True}
        if with_date:
            mapping['detail'] = {'name': 'range', 'type': 'html'}

        # Bypassing the access rigths of partner to search the address.
        def search_in_address(env, search_term):
            ret = env['event.type'].sudo()._search([
                ('address_search', 'ilike', search_term),
            ])
            return [('id', 'in', ret)]

        return {
            'model': 'event.type',
            'base_domain': domain,
            'search_fields': search_fields,
            'fetch_fields': fetch_fields,
            'mapping': mapping,
            'icon': 'fa-ticket',
            'current_date': current_date,
            'search_tags': search_tags,
            'no_date_domain': no_date_domain,
            'no_country_domain': no_country_domain,
        }
