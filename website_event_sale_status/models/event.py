from odoo import fields, models, _, api
from datetime import datetime, timedelta
import logging
import pytz
from pytz import timezone
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
_logger = logging.getLogger(__name__)


class EventEvent(models.Model):
    _inherit = "event.event"

