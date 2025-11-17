from odoo import models, fields, api, _


class SlideChannelPartner(models.Model):
    _inherit = 'slide.channel.partner'

    employee_id = fields.Many2one(
        'hr.employee',
        string="Employee",
        related='partner_id.employee_id',
        store=True,
        readonly=True
    )
