from odoo import models, api, fields, SUPERUSER_ID
from odoo.addons.event.models.event_mail import _INTERVALS


class TriggerEvent(models.Model):
    _inherit = "event.mail"

    interval_type = fields.Selection(
        selection_add=[
            ('after_confirmed_so', 'After Confirmed SO'),
            ('after_reservation_reg', 'After Reservation Registration')
        ],
        ondelete={'after_confirmed_so': 'cascade', 'after_reservation_reg': 'cascade'})

    def _compute_done(self):
        for mail in self:
            if mail.interval_type in ['before_event', 'after_event']:
                mail.done = mail.mail_sent
            else:
                mail.done = len(mail.mail_registration_ids) == len(mail.event_id.registration_ids) and all(mail.mail_sent for mail in mail.mail_registration_ids)

    def _compute_scheduled_date(self):
        for mail in self:
            if mail.interval_type in ['after_sub', 'after_confirmed_so', 'after_reservation_reg']:
                date, sign = mail.event_id.create_date, 1
            elif mail.interval_type == 'before_event':
                date, sign = mail.event_id.date_begin, -1
            else:
                date, sign = mail.event_id.date_end, 1

            mail.scheduled_date = date + _INTERVALS[mail.interval_unit](sign * mail.interval_nbr) if date else False

    def execute(self):
        for mail in self:
            now = fields.Datetime.now()
            if mail.interval_type == 'after_sub':
                # update registration lines
                lines = [
                    (0, 0, {'registration_id': registration.id})
                    for registration in (mail.event_id.registration_ids - mail.mapped('mail_registration_ids.registration_id'))
                ]
                if lines:
                    mail.write({'mail_registration_ids': lines})
                # execute scheduler on registrations
                mail.mail_registration_ids.execute()
            elif mail.interval_type == 'after_confirmed_so':
                lines = [
                    (0, 0, {'registration_id': registration.id})
                    for registration in mail.event_id.registration_ids - mail.mapped('mail_registration_ids.registration_id')
                    if registration.sale_order_id.state in ['sale', 'done']
                ]
                if lines:
                    mail.write({'mail_registration_ids': lines})
                mail.mail_registration_ids.execute()
            elif mail.interval_type == 'after_reservation_reg':
                lines = [
                    (0, 0, {'registration_id': registration.id})
                    for registration in mail.event_id.registration_ids.filtered(
                        lambda reg: reg.state == 'reservation') - mail.mapped('mail_registration_ids.registration_id')
                ]
                if lines:
                    mail.write({'mail_registration_ids': lines})
                mail.mail_registration_ids.execute()
            else:
                # Do not send emails if the mailing was scheduled before the event but the event is over
                if not mail.mail_sent and mail.scheduled_date <= now and mail.notification_type == 'mail' and \
                        (mail.interval_type != 'before_event' or mail.event_id.date_end > now):
                    mail.event_id.mail_attendees(mail.template_id.id)
                    mail.write({'mail_sent': True})
        return True


class TriggerEventType(models.Model):
    _inherit = "event.type.mail"

    interval_type = fields.Selection(
        selection_add=[('after_confirmed_so', 'After Confirmed SO'),
                       ('after_reservation_reg', 'After Reservation Registration')],
        ondelete={'after_confirmed_so': 'cascade'})


class EventRegistration(models.Model):
    _inherit = "event.registration"

    def write(self, vals):
        ret = super(EventRegistration, self).write(vals)

        if vals.get('state') == 'open':
            # auto-trigger after_sub (on subscribe) mail schedulers, if needed
            onsubscribe_schedulers = self.mapped('event_id.event_mail_ids').filtered(
                lambda s: s.interval_type in ['after_sub', 'after_confirmed_so']
            )
            onsubscribe_schedulers.with_user(SUPERUSER_ID).execute()

        if vals.get('state') == 'reservation':
            onsubscribe_schedulers = self.mapped('event_id.event_mail_ids').filtered(
                lambda s: s.interval_type == 'after_reservation_reg'
            )
            onsubscribe_schedulers.with_user(SUPERUSER_ID).execute()

        return ret