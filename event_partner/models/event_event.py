from odoo import models, fields, api, _


class EventEvent(models.Model):
    _inherit = 'event.event'

    res_partner_ids = fields.Many2many('res.partner', string="Partners")
