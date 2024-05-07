from odoo import _, api, fields, models


class EventEvent(models.Model):
    """Event"""
    _inherit = 'event.event'

    state_id = fields.Many2one(
        'res.country.state', 'State', related='address_id.state_id', readonly=False, store=True)

