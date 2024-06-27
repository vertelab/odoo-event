# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)
class HrEmployee(models.Model):
     _inherit="hr.employee"
     
    #  subordinate_course_participations_ids = fields.One2many('slide.channel.partner', string='Subordinate course participations',compute="")
    #  subordinate_course_participations_amount = fields.Integer(string="Number of subordinate course participations")
     
    #  def compute_subordinate_course_participations(self):
    #      subordinate_subscribed_courses = self.child_ids.subscribed_courses
    #      subordinate_partner_ids = self.child_ids.user_partner_id
    #      #subordinate_course_participations = self.env['slide.channel.partner'].search([('partner_id.id','in',[subordinate_partner_ids.ids])]) 
    #      subordinate_course_participations = self.env['slide.channel.partner'].search([('partner_id.id','in',subordinate_partner_ids.ids)]).ids

     def manager_course_overview(self):
         subordinate_partner_ids = self.child_ids.user_partner_id
         #subordinate_course_participations = self.env['slide.channel.partner'].search([('partner_id.id','in',[subordinate_partner_ids.ids])]) 
         subordinate_course_participations = self.env['slide.channel.partner'].search([('partner_id.id','in',subordinate_partner_ids.ids)]).ids
         

         
         return {
            'type': 'ir.actions.act_window',
            'name': 'Subordinate Course Participations',
            'view_mode': 'kanban,form',
            'res_model': 'slide.channel.partner',
            'domain': [('id', 'in', subordinate_course_participations)],
            'context': {'group_by': 'partner_id'},
            'target': 'current',
        }
