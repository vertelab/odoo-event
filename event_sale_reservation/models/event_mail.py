from odoo import models, api, fields


class EventEvent(models.Model):
    _inherit = 'event.event'

    def mail_attendees(self, template_id, force_send=False, filter_func=lambda self: self.state not in ['cancel', 'reservation']):
        for event in self:
            for attendee in event.registration_ids.filtered(filter_func):
                self.env['mail.template'].browse(template_id).send_mail(attendee.id, force_send=force_send)


