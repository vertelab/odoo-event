from odoo import models, api, fields, _


class EventEvent(models.Model):
    _inherit = 'event.event'

    event_publish_date = fields.Date(string="Publish On")
    event_un_publish_date = fields.Date(string="Un-Publish On")

    @api.model
    def create(self, vals):
        res = super(EventEvent, self).create(vals)
        if vals.get('event_publish_date'):
            pub_date_dt = fields.Date.from_string(vals.get('event_publish_date'))
            vals['website_published'] = pub_date_dt == fields.Date.today()
        return res

    def write(self, value):
        res = super(EventEvent, self).write(value)
        if self.event_publish_date and not self.website_published:
            self.website_published = self.event_publish_date == fields.Date.today()
        return res

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
