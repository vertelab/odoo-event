from odoo import models, fields, api, _


class Event(models.Model):
    _inherit = 'event.event'

    employee_skill_ids = fields.One2many('hr.employee.skill', 'event_id', string="Skills")
    skill_ids = fields.Many2many('hr.skill', compute='_compute_skill_ids', store=True)

    @api.depends('employee_skill_ids.skill_id')
    def _compute_skill_ids(self):
        for employee in self:
            employee.skill_ids = employee.employee_skill_ids.skill_id
