from odoo import models, fields, api


class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    target_demographic_id = fields.Many2one(
        "event.target.demographic", string="Target Demographic",
        store=True
    )