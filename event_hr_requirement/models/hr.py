from odoo import models, fields, api, _


class EmployeeSkills(models.Model):
    _inherit = 'hr.employee.skill'

    event_id = fields.Many2one('event.event', string="Event")
    event_type_id = fields.Many2one('event.type', string="Event Template")
    employee_id = fields.Many2one('hr.employee', required=False, ondelete='cascade')
    
    
    #These dont work.
    _sql_constraints = [
        ('_unique_skill', 'unique (employee_id, skill_id, event_id, event_type_id)', "Two levels for the same skill is not allowed"),
    ]
    
    _sql_constraints = [
        ('_unique_skill_event', 'unique (skill_id, event_id)', "Two levels for the same skill is not allowed"),
    ]
    
    _sql_constraints = [
        ('_unique_skill_event_type', 'unique (skill_id, event_type_id)', "Two levels for the same skill is not allowed"),
    ]
