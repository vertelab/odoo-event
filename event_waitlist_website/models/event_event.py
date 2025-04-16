# # if VERSION <= 17.0
from odoo.addons.website.models.website import slug
# #else
from odoo import models, fields, api, _, SUPERUSER_ID
# #endif

import logging
_logger = logging.getLogger(__name__)

class EventEvent(models.Model):
    _inherit = 'event.event'	

    full_website_url = fields.Char(
        compute="_compute_full_website_url_field", string="The actual full url for the website"
    )

    @api.depends("full_website_url")
    def _compute_full_website_url_field(self):
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')

        for event in self:
            event.full_website_url = False
            event_url = event.website_url
            if base_url and event_url:
                event.full_website_url = f"{base_url}{event_url}"

    @api.model_create_multi
    def create(self, vals_list):
        events = super(EventEvent, self).create(vals_list)

        for event in events:
            waiting_list_ids = self.env['event.waiting.list'].search([('event_type_id', '=', event.event_type_id.id)])
            _logger.warning(f"waiting_list_ids {waiting_list_ids=}")

            if not waiting_list_ids:
                onsubscribe_schedulers = event.event_mail_ids.filtered(
                    lambda event_mail: event_mail.interval_type == 'open_event_slot'
                )

                _logger.warning(f"onsubscribe_schedulers {onsubscribe_schedulers=}")
                onsubscribe_schedulers.with_user(SUPERUSER_ID).execute()
        return events
