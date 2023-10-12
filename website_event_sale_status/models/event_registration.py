from odoo import fields, models, _
import datetime
import logging
_logger = logging.getLogger(__name__)


class EventRegistrationCron(models.Model):
    _inherit = "event.registration"

    def cron_remove_tentative_registrations(self):
        registration_search = self.env['event.registration'].search([('visitor_id', '!=', False), ('state', '=', 'draft')])
        registration_search_filtered = registration_search.filtered(lambda x: x.event_id.stage_id.name in ('Ny', 'Publicerad', 'Inbjudan skickad') and x.event_id.active == True)
        _logger.warning(f"The following event.registration are deemed 'incomplete' ones, and will be removed if they are too old: {registration_search_filtered}")
        for registration in registration_search_filtered:
            #if registration.date_open <= datetime.datetime.utcnow() - datetime.timedelta(hours=1):
            if registration.date_open <= datetime.datetime.utcnow() - datetime.timedelta(minutes=5):
                if registration.sale_order_id.invoice_ids:
                    _logger.error(f"This event.registration was deemed 'incomplete' and too old, but had a invoice, and could not be removed: {registration}")
                else:
                        _logger.warning(f"This event.registration was deemed 'incomplete' and too old, and canceled: {registration}")
                        registration.action_cancel()
                        registration.sale_order_id.state = "cancel"
