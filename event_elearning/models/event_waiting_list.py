from odoo import models, fields, api, _

class Event(models.Model):
    _inherit = 'event.waiting.list'

    full_web_url = fields.Char(compute="_compute_full_web_url_field", string="The complet url for the website")

    @api.depends("full_web_url")
    def _compute_full_web_url_field(self):

        self.full_web_url = False

        base_url = self.env['ir.config_parameter'].get_param('web.base.url')

        event_url = self.search

        if base_url and event_url:

            self.full_web_url = f"{base_url}{event_url}"
