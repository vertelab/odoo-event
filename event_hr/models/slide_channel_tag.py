from odoo import models, fields, api, _


class SlideChannelTag(models.Model):
    _inherit = 'slide.channel.tag'

    survey_survey_ids = fields.Many2many(
        'survey.survey', 'survey_channel_tag_rel', 'tag_id', 'survey_id', string='Certificate')