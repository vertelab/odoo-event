from odoo import models, api, fields, SUPERUSER_ID
from odoo.addons.event.models.event_mail import _INTERVALS
import logging

class TriggerEvent(models.Model):
    _inherit = "event.mail"

    interval_type = fields.Selection(
        selection_add=[
            ('after_confirmed_so', 'After Confirmed Sale Order'),
            ('after_reservation_reg', 'After Reservation Registration')
        ],
        ondelete={'after_confirmed_so': 'cascade', 'after_reservation_reg': 'cascade'})

    @api.depends('event_id.date_begin', 'event_id.date_end', 'interval_type', 'interval_unit', 'interval_nbr')
    def _compute_scheduled_date(self):
        for scheduler in self:
            if scheduler.interval_type in ['after_sub', 'after_confirmed_so', 'after_reservation_reg']:
                date, sign = scheduler.event_id.create_date, 1
            elif scheduler.interval_type == 'before_event':
                date, sign = scheduler.event_id.date_begin, -1
            else:
                date, sign = scheduler.event_id.date_end, 1

            scheduler.scheduled_date = date.replace(microsecond=0) + _INTERVALS[scheduler.interval_unit](sign * scheduler.interval_nbr) if date else False

    @api.depends('interval_type', 'mail_done')
    def _compute_mail_state(self):
        for scheduler in self:
            if scheduler.interval_type in ('after_sub', 'after_confirmed_so', 'after_reservation_reg'):
                scheduler.mail_state = 'running'
            elif scheduler.mail_done:
                scheduler.mail_state = 'sent'
            else:
                scheduler.mail_state = 'scheduled'

    def execute(self):
        now = fields.Datetime.now()
        for scheduler in self._filter_template_ref():
            if scheduler.interval_type == 'after_sub':
                scheduler._execute_attendee_based()
            elif scheduler.interval_type == 'after_confirmed_so':
                scheduler._execute_confirmed_so_based()
            elif scheduler.interval_type == 'after_reservation_reg':
                scheduler._execute_reservation_based()
            else:
                # before_event / after_event — single-shot
                if scheduler.mail_done:
                    continue
                if scheduler.scheduled_date <= now and (
                    scheduler.interval_type != 'before_event' or scheduler.event_id.date_end > now
                ):
                    scheduler._execute_event_based()
        return True

    def _execute_confirmed_so_based(self):
        self.ensure_one()
        registrations = self.event_id.registration_ids.filtered(
            lambda r: r.sale_order_id.state in ('sale', 'done')
        )
        self._execute_registration_based(registrations)

    def _execute_reservation_based(self):
        self.ensure_one()
        registrations = self.event_id.registration_ids.filtered(
            lambda r: r.state == 'reservation'
        )
        self._execute_registration_based(registrations)

    def _execute_registration_based(self, registrations):
        self.ensure_one()
        already_linked = self.mapped('mail_registration_ids.registration_id')
        new_registrations = registrations - already_linked

        if new_registrations:
            self._create_missing_mail_registrations(new_registrations)

        self.with_context(
            event_mail_registration_ids=registrations.ids
        ).mail_registration_ids.filtered(
            lambda r: r.registration_id in registrations
        ).execute()

        self._refresh_mail_count_done()


class TriggerEventType(models.Model):
    _inherit = "event.type.mail"

    interval_type = fields.Selection(
        selection_add=[('after_confirmed_so', 'After Confirmed Sale Order'),
                       ('after_reservation_reg', 'After Reservation Registration')],
        ondelete={'after_confirmed_so': 'cascade', 'after_reservation_reg': 'cascade'})


class EventRegistration(models.Model):
    _inherit = "event.registration"

    @api.model_create_multi
    def create(self, vals_list):
        registrations = super().create(vals_list)
        reservation_regs = registrations.filtered(lambda r: r.state == 'reservation')
        if reservation_regs:
            schedulers = reservation_regs.mapped('event_id.event_mail_ids').filtered(
                lambda s: s.interval_type == 'after_reservation_reg'
            )
            schedulers.with_user(SUPERUSER_ID).with_context(
                event_mail_registration_ids=reservation_regs.ids
            ).execute()
        return registrations

    def write(self, vals):
        ret = super().write(vals)
        if vals.get('state') == 'open':
            schedulers = self.mapped('event_id.event_mail_ids').filtered(
                lambda s: s.interval_type in ('after_sub', 'after_confirmed_so')
            )
            schedulers.with_user(SUPERUSER_ID).with_context(
                event_mail_registration_ids=self.ids
            ).execute()
        return ret


class EventMailRegistration(models.Model):
    _inherit = "event.mail.registration"

    def _get_skip_domain(self):
        domain = super()._get_skip_domain()
        if any(r.scheduler_id.interval_type == 'after_reservation_reg' for r in self):
            domain = [d for d in domain if 'registration_id.state' not in str(d)]
            domain += [('registration_id.state', 'in', ('open', 'done', 'reservation'))]
        return domain