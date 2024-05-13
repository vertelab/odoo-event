from odoo import models, fields, api, _


class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    validity = fields.Integer(string="Course Validity")

