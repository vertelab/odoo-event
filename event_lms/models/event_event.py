from odoo import models, fields, api, _

class EventEvent(models.Model):
    _inherit = 'event.event'

    slide_channel_id = fields.Many2one(
        string="Slide Channel", comodel_name="slide.channel", compute='_compute_slide_channel', precompute=True, readonly=False, store=True)

    @api.depends('event_type_id')
    def _compute_slide_channel(self):
        for event in self:
            if event.event_type_id.slide_channel_id:
                event.slide_channel_id = event.event_type_id.slide_channel_id

    
