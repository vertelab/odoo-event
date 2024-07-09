import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class EventRegistration(models.Model):
    _inherit = 'event.registration'
    meeting_event_url = fields.Char(related='event_id.meeting_event_url')
