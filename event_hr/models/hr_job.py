# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Job(models.Model):
    _inherit = "hr.job"

    mandatory_event_ids = fields.Many2many(
        'event.type', 'hr_job_mandatory_event_ids', 'job_id', 'event_id',
        string='Mandatory Courses',  help="Mandatory Courses for this position")

    event_ids = fields.Many2many(comodel_name='event.type', string='Other Courses',
                                 help="Other Courses for this position")

    mandatory_survey_ids = fields.Many2many('survey.survey', string="Survey")

    mandatory_slide_channel_ids = fields.Many2many('slide.channel', string="Courses")

    resume_renewal = fields.Integer(string="Days to Recommendation")
