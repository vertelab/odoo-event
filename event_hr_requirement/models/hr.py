from odoo import models, fields, api, _


class EmployeeSkills(models.Model):
    _inherit = 'hr.employee.skill'

    event_id = fields.Many2one('event.event', string="Event")
