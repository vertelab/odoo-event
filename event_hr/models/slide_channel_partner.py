from odoo import models, fields, api, _


class SlideChannelPartner(models.Model):
    _inherit = 'slide.channel.partner'

    employee_job_id = fields.Many2one(
        'hr.job',
        string="Employee Job",
        related='partner_id.employee_id.job_id',
        store=True,
        readonly=True
    )

    employee_department_id = fields.Many2one(
        'hr.department',
        string="Employee Department",
        related='partner_id.employee_id.department_id',
        store=True,
        readonly=True
    )