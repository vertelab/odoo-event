import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class event(models.Model):
    _inherit = 'event.event'
    meeting_event_url = fields.Char(string="Web meeting url")
