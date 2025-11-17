from datetime import date, timedelta
from odoo import models, fields, api, _
from odoo.tools import html2plaintext
from odoo.addons.hr_skills_survey.models.survey_user import SurveyUserInput as SurveyUserInputOG
import logging
_logger = logging.getLogger(__name__)

class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    def _mark_done(self):
        """ Will add certification to employee's resume if
        - The survey is a certification
        - The user is linked to an employee
        - The user succeeded the test """

        super(SurveyUserInputOG, self)._mark_done()

        certification_user_inputs = self.filtered(
            lambda user_input: user_input.survey_id.certification and user_input.scoring_success)
        partner_has_completed = {user_input.partner_id.id: user_input.survey_id for user_input in
                                 certification_user_inputs}
        employees = self.env['hr.employee'].sudo().search(
            [('user_id.partner_id', 'in', certification_user_inputs.mapped('partner_id').ids)])
        resume_lines = self.env['hr.resume.line']
        for employee in employees:
            line_type = self.env.ref('hr_skills_survey.resume_type_certification', raise_if_not_found=False)
            survey = partner_has_completed.get(employee.user_id.partner_id.id)
            resume_lines = resume_lines + self.env['hr.resume.line'].create({
                'employee_id': employee.id,
                'name': survey.title,
                'date_start': fields.Date.today(),
                'date_end': fields.Date.today() + timedelta(days=survey.validity),
                'description': html2plaintext(survey.description),
                'line_type_id': line_type and line_type.id,
                'display_type': 'certification',
                'survey_id': survey.id
            })
        return resume_lines


class Survey(models.Model):
    _inherit = 'survey.survey'

    lead_time = fields.Integer(string="Lead Time")
    validity = fields.Integer(string="Course Validity")


class MandatoryEdu(models.TransientModel):
    _name = "mandatory.edu"
    
    def action_view_course(self):
        self.ensure_one()
        if self.edu_source_reference:
            _logger.warning(f"{self.edu_source_reference=}")
            return {
                'type': 'ir.actions.act_window',
                'name': 'View Course',
                'res_model': self.edu_source_reference._name,
                'res_id': self.edu_source_reference.id,
                'view_mode': 'form',
                'target': 'current',
            }
        return False

    @api.model
    def _selection_reference_model(self):
        return [('event.type', 'Course'), ('survey.survey', 'Survey'), ('slide.channel', 'Course')]

    edu_reference = fields.Reference(selection=_selection_reference_model, readonly=True, string="Course Name")

    def _selection_source_model(self):
        return [('survey.survey', 'Survey'), ('slide.channel', 'Course')]

    edu_source_reference = fields.Reference(selection=_selection_source_model, readonly=True)

    mandatory = fields.Boolean()
    employee_id = fields.Many2one(comodel_name="hr.employee")
    lead_time = fields.Integer()
    date_end = fields.Date()
