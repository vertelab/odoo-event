from odoo import models, fields, _, api
import uuid

class EventWaitingList(models.Model):
    _name = 'event.waiting.list'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Event Waiting List'
    _order = 'id desc'

    event_type_id = fields.Many2one('event.type', string='Event Type', required=True)
    event_id = fields.Many2one('event.event', string='Event')
    active = fields.Boolean(default=True)
    removal_link = fields.Char(compute="_compute_removal_link")
    unique_removal_uuid = fields.Char(compute="_compute_unique_removal_uuid", precompute=True,  store=True, string="This uuid is used to make it possible for users to unsubscribe from the waiting list")

    @api.depends('removal_link','unique_removal_uuid')
    def _compute_removal_link(self):

        base_url = self.env['ir.config_parameter'].get_param('web.base.url')

        for waiting_list_id in self:

            waiting_list_id.removal_link = f"{base_url}/event-type/waiting-list-registration/remove/{waiting_list_id.unique_removal_uuid}"


    @api.depends('unique_removal_uuid')
    def _compute_unique_removal_uuid(self):

        for waiting_list_id in self:

            if waiting_list_id.unique_removal_uuid:

                continue

            waiting_list_id.unique_removal_uuid = str(uuid.uuid4())


    # utm informations
    # utm_campaign_id = fields.Many2one('utm.campaign', 'Campaign', index=True, ondelete='set null')
    # utm_source_id = fields.Many2one('utm.source', 'Source', index=True, ondelete='set null')
    # utm_medium_id = fields.Many2one('utm.medium', 'Medium', index=True, ondelete='set null')

    # attendee
    partner_id = fields.Many2one('res.partner', string='Booked by', tracking=1)
    name = fields.Char(
        string='Name', index='trigram',
        compute='_compute_name', readonly=False, store=True, tracking=2)
    email = fields.Char(string='Email', compute='_compute_email', readonly=False, store=True, tracking=3)
    phone = fields.Char(string='Phone', compute='_compute_phone', readonly=False, store=True, tracking=4)
    company_name = fields.Char(
        string='Company Name', compute='_compute_company_name', readonly=False, store=True, tracking=5)
    company_id = fields.Many2one(
        'res.company', string='Company',
        store=True, readonly=False)

    event_organizer_id = fields.Many2one(string='Event Organizer', related='event_type_id.organizer_id', readonly=True)
    visitor_id = fields.Many2one('website.visitor', string='Visitor', ondelete='set null')

    @api.depends('partner_id')
    def _compute_email(self):
        for registration in self:
            if not registration.email and registration.partner_id:
                registration.email = registration._synchronize_partner_values(
                    registration.partner_id,
                    fnames={'email'},
                ).get('email') or False

    @api.depends('partner_id')
    def _compute_phone(self):
        for registration in self:
            if not registration.phone and registration.partner_id:
                partner_values = registration._synchronize_partner_values(
                    registration.partner_id,
                    fnames={'phone', 'mobile'},
                )
                registration.phone = partner_values.get('phone') or partner_values.get('mobile') or False

    @api.depends('partner_id')
    def _compute_company_name(self):
        for registration in self:
            if not registration.company_name and registration.partner_id:
                registration.company_name = registration._synchronize_partner_values(
                    registration.partner_id,
                    fnames={'company_name'},
                ).get('company_name') or False

    def _synchronize_partner_values(self, partner, fnames=None):
        if fnames is None:
            fnames = {'name', 'email', 'phone', 'mobile'}
        if partner:
            contact_id = partner.address_get().get('contact', False)
            if contact_id:
                contact = self.env['res.partner'].browse(contact_id)
                return dict((fname, contact[fname]) for fname in fnames if contact[fname])
        return {}

    def _get_website_registration_allowed_fields(self):
        return {'name', 'phone', 'email', 'company_name', 'event_type_id', 'partner_id'}

    def action_confirm(self):
        pass
