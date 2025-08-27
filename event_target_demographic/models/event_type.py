from odoo import models, fields, api


class EventType(models.Model):
    _inherit = 'event.type'

    target_demographic_id = fields.Many2one("event.target.demographic", string="Target Demographic")