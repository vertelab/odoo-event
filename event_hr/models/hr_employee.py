from datetime import date, timedelta
from dateutil import relativedelta
from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def action_view_recommended_certification(self):
        mandatory_edu_vals_list = []
        self.env['mandatory.edu'].search([('employee_id', '=', self.id)]).unlink()

        all_surveys = self.env['survey.user_input'].search([
            ('partner_id', '=', self.user_partner_id.id)
        ]).mapped("survey_id")

        resume_lines = self.env['hr.resume.line'].search([
            ('employee_id', '=', self.id), ('display_type', '=', 'certification'),
        ])

        mandatory_surveys = self.job_id.mandatory_survey_ids
        intersection = mandatory_surveys & all_surveys
        todo_mandatory_survey = mandatory_surveys | intersection
        todo_voluntary_certs = all_surveys - intersection
        mandatory_courses = self.job_id.mandatory_slide_channel_ids

        for cert in todo_voluntary_certs:
            event_type = self.env['event.type'].search([('slide_channel_id', 'in', cert.slide_channel_ids.ids)],
                                                       limit=1)
            latest_user_input = self.env['survey.user_input'].search([
                ('partner_id', '=', self.user_partner_id.id),
                ('survey_id', '=', cert.id), ('scoring_success', '=', True), ('state', '=', 'done')],
                order="end_datetime desc", limit=1)
            mandatory_edu_vals_list.append({
                "edu_reference": f"event.type,{event_type.id}" if event_type else f"survey.survey,{cert.id}",
                "edu_source_reference": f"survey.survey,{cert.id}",
                "employee_id": self.id,
                "mandatory": False,
                "lead_time": cert.lead_time,
                "date_end": latest_user_input.end_datetime if latest_user_input else False,

            })
        for cert in todo_mandatory_survey:
            event_type = self.env['event.type'].search([('slide_channel_id', 'in', cert.slide_channel_ids.ids)],
                                                       limit=1)
            latest_user_input = self.env['survey.user_input'].search(
                [('partner_id', '=', self.user_partner_id.id), ('survey_id', '=', cert.id),
                 ('scoring_success', '=', True), ('state', '=', 'done')], order="end_datetime desc", limit=1)
            mandatory_edu_vals_list.append({
                "edu_reference": f"event.type,{event_type.id}" if event_type else f"survey.survey,{cert.id}",
                "edu_source_reference": f"survey.survey,{cert.id}",
                "employee_id": self.id,
                "mandatory": True,
                "lead_time": cert.lead_time,
                "date_end": latest_user_input.end_datetime if latest_user_input else False,

            })

        for slide_channel_id in mandatory_courses:
            print(f"{slide_channel_id.display_name=}")
            event_type = self.env['event.type'].search([('slide_channel_id', '=', slide_channel_id.id)], limit=1)
            mandatory_edu_vals_list.append({
                "edu_reference": f"event.type,{event_type.id}" if event_type else f"slide.channel,{slide_channel_id.id}",
                "edu_source_reference": f"slide.channel,{slide_channel_id.id}",
                "employee_id": self.id,
                "mandatory": True,

            })

        edu_ids = self.env['mandatory.edu'].create(mandatory_edu_vals_list)
        return {
            'name': _('Courses'),
            'view_mode': 'tree,form',
            'domain': [('id', 'in', edu_ids.ids)],
            'res_model': 'mandatory.edu',
            'type': 'ir.actions.act_window',
        }

    # @api.depends('user_partner_id')
    # def _compute_completed_courses(self):
    #     for rec in self:
    #         if rec.user_partner_id:
    #             rec.completed_course_count = len(rec.user_partner_id.slide_channel_completed_ids)
    #             # rec.completed_course_count = self.env['slide.channel.partner'].search_count([
    #             #     ('partner_id', '=', rec.user_partner_id.id)
    #             # ])
    #         else:
    #             rec.completed_course_count = 0
    #
    # completed_course_count = fields.Integer(string="Completed Course(s)", compute=_compute_completed_courses)

    @api.depends('user_partner_id')
    def _compute_completed_certification(self):
        for rec in self:
            if rec.user_partner_id:
                rec.completed_certification_count = len(rec.user_partner_id.survey_user_input_ids)
            else:
                rec.completed_certification_count = 0

    completed_certification_count = fields.Integer(string="Completed Certification(s)",
                                                   compute=_compute_completed_certification)

    def action_view_completed_courses(self):
        pass

    def action_view_completed_certification(self):
        return {
            'name': _('Certifications'),
            'view_mode': 'tree,form',
            'domain': [('partner_id', 'in', self.user_partner_id.ids)],
            'res_model': 'survey.user_input',
            'type': 'ir.actions.act_window',
        }

    def _compute_recommended_certification(self):
        for rec in self:
            employee_slide_channel_ids = rec.user_partner_id.slide_channel_ids
            employee_certification_ids = rec.user_partner_id.survey_user_input_ids

            hr_job_mandatory_certification_ids = rec.job_id.mandatory_survey_ids
            hr_job_mandatory_slide_channel_ids = rec.job_id.mandatory_slide_channel_ids

            # recommended_certification_ids = self.env['survey.user_input']
            recommended_certification_ids = self.env['survey.survey']
            recommended_slide_channel_ids = self.env['slide.channel']

            # 1. check if mandatory certification is in employee certification
            #    if present: you want to check hr.resume for the expiration date of the certification
            #       if in hr.resume, but no expiration or not yet expired, then pass
            #       if in hr.resume, but expired, then recommend

            #

            certification_todo = hr_job_mandatory_certification_ids - employee_certification_ids.mapped('survey_id')

            for employee_certification_id in employee_certification_ids.mapped('survey_id'):
                if employee_certification_id in hr_job_mandatory_certification_ids:
                    employee_resume_certification_id = self.env['hr.resume.line'].search([
                        ('employee_id', '=', rec.id),
                        ('display_type', '=', 'certification'),
                        ('survey_id', '=', employee_certification_id.id),
                    ], order="date_end desc", limit=1)
                    print(f"{employee_resume_certification_id.name=}")
                    # renewal_reminder_date = date.today(), + timedelta(days=rec.job_id.resume_renewal)
                    if employee_resume_certification_id:
                        renewal_reminder_date = (
                                employee_resume_certification_id.date_end - timedelta(days=rec.job_id.resume_renewal)
                        )
                        print(renewal_reminder_date)
                        if date.today() >= renewal_reminder_date:
                            recommended_certification_ids |= employee_certification_id

            recommended_certification_ids |= certification_todo
            rec.recommended_certification_ids = recommended_certification_ids.ids
            rec.recommended_certification_count = len(rec.recommended_certification_ids)

    recommended_certification_count = fields.Integer(string="Completed Certification(s)",
                                                     compute=_compute_recommended_certification)

    recommended_certification_ids = fields.One2many(
        'survey.survey', string='Recommended Certifications',
        compute='_compute_recommended_certification')

    def action_view_recommended_certification_old(self):
        return {
            'name': _('Recommended Certifications'),
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.recommended_certification_ids.ids)],
            'res_model': 'survey.survey',
            'type': 'ir.actions.act_window',
        }
