from odoo import models, api, fields, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    survey_user_input_ids = fields.Many2many(
        'survey.user_input', string='Certifications',
        compute='_compute_survey_user_input_values',
        groups="website_slides.group_website_slides_officer")

    completed_survey_user_input_ids = fields.One2many(
        'survey.user_input', string='Completed Certifications',
        compute='_compute_slide_channel_values',
        search='_compute_survey_user_input_values',
        groups="website_slides.group_website_slides_officer")

    passed_survey_user_input_ids = fields.One2many(
        'survey.user_input', string='Passed Certifications',
        compute='_compute_survey_user_input_values',
        groups="website_slides.group_website_slides_officer")

    failed_survey_user_input_ids = fields.One2many(
        'survey.user_input', string='Failed Certifications',
        compute='_compute_survey_user_input_values',
        groups="website_slides.group_website_slides_officer")

    survey_user_input_count = fields.Integer(
        'Course Count', compute='_compute_survey_user_input_values',
        groups="website_slides.group_website_slides_officer")

    def _compute_survey_user_input_values(self):

        self.env['survey.user_input'].search([('partner_id', 'in', self.ids)])

        for partner in self:
            survey_user_input_ids = self.env['survey.user_input'].search([('partner_id', 'in', self.ids)])
            partner.survey_user_input_ids = survey_user_input_ids.ids

            completed_survey_user_input_ids = survey_user_input_ids.filtered(
                lambda user_input: user_input.state == 'done'
            )

            passed_survey_user_input_ids = survey_user_input_ids.filtered(
                lambda user_input: user_input.scoring_success
            )

            failed_survey_user_input_ids = survey_user_input_ids.filtered(
                lambda user_input: not user_input.scoring_success
            )
            partner.passed_survey_user_input_ids = passed_survey_user_input_ids
            partner.failed_survey_user_input_ids = failed_survey_user_input_ids
            partner.completed_survey_user_input_ids = completed_survey_user_input_ids
            partner.survey_user_input_count = len(survey_user_input_ids)

    def action_view_survey_inputs(self):
        return {
            'name': _('Certifications'),
            'view_mode': 'list,form',
            'domain': [('partner_id', 'in', self.ids)],
            'res_model': 'survey.user_input',
            'type': 'ir.actions.act_window',
        }

    employee_id = fields.Many2one(
        'hr.employee',
        string="Main Employee",
        compute='_compute_employee_id',
        search='_search_main_employee',
        store=False,
        readonly=False,
    )

    @api.depends('employee_ids')
    def _compute_employee_id(self):
        for partner in self:
            if partner.employee_ids:
                employee = partner.employee_ids[0]
            else:
                employee = False
            partner.employee_id = employee

    def _search_employee_id(self, operator, value):
        """Search for partners based on their main employee"""
        return [('employee_ids', operator, value)]

