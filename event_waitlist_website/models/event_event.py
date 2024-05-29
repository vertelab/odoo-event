from odoo import models, fields, api, _, SUPERUSER_ID
import logging
_logger = logging.getLogger(__name__)


class EventEvent(models.Model):

    _inherit = 'event.event'	

    full_website_url = fields.Char(compute="_compute_full_website_url_field", string="The actuall full url for the website")

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

        _logger.warning("event create"*100)
        events = super(EventEvent, self).create(vals_list)

        for event in events:

            waiting_list_ids = self.env['event.waiting.list'].search([('event_type_id', '=', event.event_type_id.id)])
            _logger.warning(f"waiting_list_ids {waiting_list_ids=}")

            if not waiting_list_ids:
                return

            _logger.warning(f"event {event=}")
            onsubscribe_schedulers = event.event_mail_ids.filtered(lambda event_mail: event_mail.interval_type == 'open_event_slot')

            if onsubscribe_schedulers:

                _logger.warning(f"onsubscribe_schedulers {onsubscribe_schedulers=}")
                onsubscribe_schedulers.with_user(SUPERUSER_ID).execute()

        return events


    # @api.model_create_multi
    # def create(self, vals_list):

    #     events = super(EventEvent, self).create(vals_list)

    #     for event in events:

    #         waiting_list_ids = self.env['event.waiting.list'].search([('event_type_id', '=', event.event_type_id.id)])

    #         if not waiting_list_ids:
    #             continue

    #         _logger.warning(f"event {event=}")
    #         onsubscribe_schedulers = event.event_mail_ids.filtered(lambda event_mail: event_mail.interval_type == 'open_event_slot')

    #         for onsubscribe_scheduler in onsubscribe_schedulers:

    #             # onsubscribe_scheduler._create_missing_mail_registrations(waiting_list_ids)

    #             new_mails = []

    #             for waiting_list_id in waiting_list_ids:

    #                 _logger.warning(f"{waiting_list_id.name=}" * 500)
    #                 new_mails.append({'registration_id': waiting_list_id.id,'scheduler_id': onsubscribe_scheduler.id,})

    #             self.env['event.mail.registration'].create(new_mails)

    #         all_mail_done = all(mail_registration.mail_sent == True for mail_registration in onsubscribe_scheduler.mail_registration_ids)
    #         total_sent = len(onsubscribe_scheduler.mail_registration_ids.filtered(lambda reg: reg.mail_sent))

    #         onsubscribe_scheduler.update({
    #             'mail_done': all_mail_done,
    #             'mail_count_done': total_sent
    #         })
    #         # _logger.warning(f"onsubscribe_schedulers {onsubscribe_schedulers=}")
    #         # onsubscribe_schedulers.with_user(SUPERUSER_ID).execute()

    #     return events