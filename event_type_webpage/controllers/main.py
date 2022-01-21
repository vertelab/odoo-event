# -*- coding: utf-8 -*-

import werkzeug
from werkzeug.exceptions import NotFound

from odoo import fields, http, _
from odoo.http import request


class WebsiteEventTypeController(http.Controller):

    @http.route(['''/event-type/<model("event.type"):event_type>'''], type='http', auth="public", website=True, sitemap=True)
    def event_type(self, event_type, **post):
        if not event_type.can_access_from_current_website():
            raise werkzeug.exceptions.NotFound()
        return request.render("event_type_webpage.event_type_template", {'event_type': event_type})
