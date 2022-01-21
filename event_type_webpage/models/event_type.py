from odoo import models, fields, api, _
from odoo.addons.http_routing.models.ir_http import slug


class EventType(models.Model):
    _name = 'event.type'
    _inherit = ["event.type", "website.published.multi.mixin"]

    def _default_cover_properties(self):
        res = super()._default_cover_properties()
        res['opacity'] = '0.4'
        return res

    website_published = fields.Boolean(tracking=False)

    @api.depends('name')
    def _compute_website_url(self):
        super(EventType, self)._compute_website_url()
        for event_type in self:
            if event_type.id:
                event_type.website_url = '/event-type/%s' % slug(event_type)
