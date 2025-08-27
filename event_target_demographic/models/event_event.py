from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    target_demographic_id = fields.Many2one(
        "event.target.demographic", string="Target Demographic",
        related="event_type_id.target_demographic_id", store=True
    )