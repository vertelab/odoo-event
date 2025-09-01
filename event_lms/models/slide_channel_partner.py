from odoo import models, fields, api, _

class SlideChannelPartner(models.Model):
    _inherit = 'slide.channel.partner'

    event_registration_ids = fields.One2many('event.registration', 'slide_channel_partner_id', 'Events Registrations')



