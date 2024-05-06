from ast import literal_eval
from dateutil.relativedelta import relativedelta
import json
import werkzeug.urls

from pytz import utc, timezone

from odoo import models, fields, api, _
from odoo.addons.http_routing.models.ir_http import slug
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
        event_waitlist_tree_view = self.env.ref('event_waitlist_website.view_event_waiting_tree')
        return {
            'name': _('Waiting List'),
            'domain': [('event_type_id', '=', self.id)],
            'res_model': 'event.waiting.list',
            'type': 'ir.actions.act_window',
            'view_id': event_waitlist_tree_view.id,
            'views': [(event_waitlist_tree_view.id, 'tree'), (False, 'form')],
            'view_mode': 'tree,form',
            'context': "{'default_event_type_id_id': %d}" % self.id
        }

    # date_begin = fields.Datetime(string='Start Date', required=False, tracking=True
    #                              , default=lambda self: fields.Datetime.now())
    # date_end = fields.Datetime(string='End Date', required=False, tracking=True,
    #                            default=lambda self: fields.Datetime.now())
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

    # def _get_event_resource_urls(self):
    #     url_date_start = self.date_begin.astimezone(timezone(self.date_tz)).strftime('%Y%m%dT%H%M%S')
    #     url_date_stop = self.date_end.astimezone(timezone(self.date_tz)).strftime('%Y%m%dT%H%M%S')
    #     params = {
    #         'action': 'TEMPLATE',
    #         'text': self.name,
    #         'dates': f'{url_date_start}/{url_date_stop}',
    #         'ctz': self.date_tz,
    #         'details': self.name,
    #     }
    #     if self.address_id:
    #         params.update(location=self.address_inline)
    #     encoded_params = werkzeug.urls.url_encode(params)
    #     google_url = GOOGLE_CALENDAR_URL + encoded_params
    #     iCal_url = f'/event/{self.id:d}/ics?{encoded_params}'
    #     return {'google_url': google_url, 'iCal_url': iCal_url}

    def _default_cover_properties(self):
        res = super()._default_cover_properties()
        res['opacity'] = '0.4'
        return res

    # website
    website_published = fields.Boolean(tracking=True)
    website_menu = fields.Boolean(
        string='Website Menu',
        compute='_compute_website_menu', precompute=True, readonly=False, store=True,
        help="Allows to display and manage event-specific menus on website.")
    menu_id = fields.Many2one('website.menu', 'Event Menu', copy=False)
    # menu_register_cta = fields.Boolean(
    #     'Extra Register Button', compute='_compute_menu_register_cta',
    #     readonly=False, store=True)
    # sub-menus management
    introduction_menu = fields.Boolean(
        "Introduction Menu", compute="_compute_website_menu_data",
        readonly=False, store=True)
    introduction_menu_ids = fields.One2many(
        "website.event.menu", "event_id", string="Introduction Menus",
        domain=[("menu_type", "=", "introduction")])
    location_menu = fields.Boolean(
        "Location Menu", compute="_compute_website_menu_data",
        readonly=False, store=True)
    location_menu_ids = fields.One2many(
        "website.event.menu", "event_id", string="Location Menus",
        domain=[("menu_type", "=", "location_menu")])
    address_name = fields.Char(related='address_id.name')

    # is_one_day = fields.Boolean(compute='_compute_field_is_one_day')

    organizer_id = fields.Many2one(
        'res.partner', string='Organizer', tracking=True,
        default=lambda self: self.env.company.partner_id,
        check_company=True)

    # @api.depends('date_begin', 'date_end', 'date_tz')
    # def _compute_field_is_one_day(self):
    #     for event in self:
    #         # Need to localize because it could begin late and finish early in
    #         # another timezone
    #         event = event._set_tz_context()
    #         begin_tz = fields.Datetime.context_timestamp(event, event.date_begin)
    #         end_tz = fields.Datetime.context_timestamp(event, event.date_end)
    #         event.is_one_day = (begin_tz.date() == end_tz.date())

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

    @api.depends("website_menu")
    def _compute_website_menu_data(self):
        """ Synchronize with website_menu at change and let people update them
        at will afterwards. """
        for event in self:
            event.introduction_menu = event.website_menu
            event.location_menu = event.website_menu
            # event.register_menu = event.website_menu

    @api.depends('name')
    def _compute_website_url(self):
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
        # dates = self._search_build_dates()
        current_date = None
        # for date_details in dates:
        #     if date == date_details[0]:
        #         domain.append(date_details[2])
        #         no_country_domain.append(date_details[2])
        #         if date_details[0] != 'upcoming':
        #             current_date = date_details[1]

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
            # 'search_extra': search_in_address,
            'fetch_fields': fetch_fields,
            'mapping': mapping,
            'icon': 'fa-ticket',
            # for website_event main controller:
            # 'dates': dates,
            'current_date': current_date,
            'search_tags': search_tags,
            'no_date_domain': no_date_domain,
            'no_country_domain': no_country_domain,
        }
