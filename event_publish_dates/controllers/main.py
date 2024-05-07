import odoo

from odoo import http, models, fields, _
from odoo.http import request

from odoo.addons.website.controllers.main import Website


class Event(Website):

    @http.route(['/website/publish'], type='json', auth="user", website=True)
    def publish(self, id, object):
        Model = request.env[object]
        record = Model.browse(int(id))

        values = {}
        if 'website_published' in Model._fields:
            values['website_published'] = not record.website_published
            record.write(values)
            try:
                Model._set_event_stages(record)
            except Exception as e:
                pass
            return bool(record.website_published)
        return False
