# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class Job(models.Model):

    _inherit = "hr.job"
    
    mandatory_event_ids = fields.Many2many(comodel_name='event.type',string='Mandatory Courses',help="Mandatory Courses for this position") 
    event_ids = fields.Many2many(comodel_name='event.type',string='Other Courses',help="Other Courses for this position") 

    
