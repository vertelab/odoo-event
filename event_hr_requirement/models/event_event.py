from odoo import models, fields, api, _
from odoo.tools import slug

class Event(models.Model):
    _inherit = 'event.event' 
    event_required_event_type_ids = fields.Many2many('event.type', string="Event Templates")
    employee_skill_ids = fields.One2many('hr.employee.skill', 'event_id', string="Skills")
    skill_ids = fields.Many2many('hr.skill', compute='_compute_skill_ids', store=True)

    @api.depends('employee_skill_ids.skill_id')
    def _compute_skill_ids(self):
        for employee in self:
            employee.skill_ids = employee.employee_skill_ids.skill_id
            
    @api.onchange("event_type_id")
    def _set_required_skills_and_event_type(self):
            for record in self:
                if record.event_type_id:
                    self.event_required_event_type_ids = self.event_type_id.event_type_required_event_type_ids
                    self.employee_skill_ids = False
                    for employee_skill in self.event_type_id.employee_skill_ids:
                        record.write({"employee_skill_ids":[(0, 0, {
                                'skill_id':employee_skill.skill_id.id,
                                'skill_level_id':employee_skill.skill_level_id.id,
                                'skill_type_id':employee_skill.skill_type_id.id,
                                'employee_id':employee_skill.employee_id.id
                        })]})
                        
                   
                    #self.skill_ids = self.event_type_id.skill_ids

            
            
class EventType(models.Model):
    _inherit = 'event.type'
    
    #required_event_type_ids = fields.Many2many(comodel_name='event.type', relation='required_event_type_rel', column1='event_type_requirments1', column2='event_type_requirments2', string="Event Templates")
    employee_skill_ids = fields.One2many('hr.employee.skill', 'event_type_id', string="Skills")
    skill_ids = fields.Many2many('hr.skill', compute='_compute_skill_ids', store=True)
    
    
    event_type_required_event_type_ids = fields.Many2many(comodel_name='event.type', relation='required_event_type_rel',
                                              column1='event_type_requirments1', column2='event_type_requirments2',
                                              string='Event Templates',
                                              )


    @api.depends('employee_skill_ids.skill_id')
    def _compute_skill_ids(self):
        for employee in self:
            employee.skill_ids = employee.employee_skill_ids.skill_id
