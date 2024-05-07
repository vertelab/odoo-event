from odoo import fields, models, _, api
from datetime import datetime, timedelta
import logging
import pytz
from pytz import timezone
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
_logger = logging.getLogger(__name__)


class EventEvent(models.Model):
    _inherit = "event.event"

    def write(self, vals):
        res = super().write(vals)
        if not self.website_published:
            registration_search = self.env['event.registration'].search([
                ('visitor_id', '!=', False), ('state', '=', 'draft'), ('event_id', '=', self.id)
            ])
            registration_search.action_cancel()
            registration_search.sale_order_id.state = "cancel"
        return res

