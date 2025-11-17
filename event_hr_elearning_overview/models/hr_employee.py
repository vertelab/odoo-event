# -*- coding: utf-8 -*-

from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    @api.depends('subordinate_course_participants_ids', 'name')
    def compute_subordinate_course_participants(self):
        for rec in self:
            subordinate_partner_ids = self.child_ids.user_partner_id
            subordinate_course_participants = self.env['slide.channel.partner'].search(
                [('partner_id.id', 'in', subordinate_partner_ids.ids)]).ids
            rec.subordinate_course_participants_ids = subordinate_course_participants
            rec.subordinate_course_participants_count = len(rec.subordinate_course_participants_ids)

    subordinate_course_participants_ids = fields.One2many(
        'slide.channel.partner',
        'employee_id',
        string='Subordinate Course Participants',
        compute='compute_subordinate_course_participants'
    )

    subordinate_course_participants_count = fields.Integer(
        string="Number of subordinate course Participants",
        compute='compute_subordinate_course_participants'
    )

    def manager_course_overview(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Subordinate Course Participation',
            'view_mode': 'kanban,form',
            'res_model': 'slide.channel.partner',
            'domain': [('id', 'in', self.subordinate_course_participants_ids.ids)],
            'context': {'group_by': 'partner_id'},
            'target': 'current',
        }
