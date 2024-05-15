from odoo import models, fields, api, _

class SlideChannel(models.Model):
    _inherit = 'slide.channel'
    event_event_ids = fields.One2many('event.event', 'slide_channel_id', 'Events')

