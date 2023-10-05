from odoo import fields, models, _
from datetime import datetime, timedelta
import logging
import pytz
from pytz import timezone
from odoo.tools.misc import DEFAULT_SERVER_DATETIME_FORMAT
_logger = logging.getLogger(__name__)


class EventRegistrationCron(models.Model):
    _inherit = "event.registration"

    def cron_remove_tentative_registrations(self):
        registration_search = self.env['event.registration'].search([
            ('visitor_id', '!=', False), ('state', '=', 'draft')
        ])
        registration_search_filtered = registration_search.filtered(
            lambda x: x.event_id.active and x.event_id.website_published)
        _logger.warning(f"The following event.registration are deemed 'incomplete' ones, and will be removed if they "
                        f"are too old: {registration_search_filtered}")
        for registration in registration_search_filtered:
            event_time_zone = pytz.timezone(registration.event_id.date_tz)
            registration_date_open = registration.date_open.astimezone(event_time_zone)

            if registration_date_open <= datetime.now().astimezone(event_time_zone) - timedelta(hours=1):
                if registration.sale_order_id.invoice_ids:
                    _logger.error(f"This event.registration was deemed 'incomplete' and too old, but had a invoice, "
                                  f"and could not be removed: {registration}")
                else:
                    _logger.warning(f"This event.registration was deemed 'incomplete' and too old, and canceled: {registration}")
                    registration.action_cancel()
                    registration.sale_order_id.state = "cancel"
