from odoo import models, api, fields, _


class EventEvent(models.Model):
    _inherit = 'event.event'

    event_publish_date = fields.Date(string="Publish On")
    event_un_publish_date = fields.Date(string="Un-Publish On")

    def _cron_publish_event(self):
        recs = self.search(
            [('website_published', '=', False),
             ('event_publish_date', '=', fields.Date.today())])
        if len(recs):
            return recs.write({'website_published': True})
        return True

    def _cron_un_publish_event(self):
        recs = self.search(
            [('website_published', '=', True),
             ('event_un_publish_date', '<=', fields.Date.today())])
        if len(recs):
            return recs.write({'website_published': False})
        return True
