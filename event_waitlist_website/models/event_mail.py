import logging
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import MissingError, ValidationError

_logger = logging.getLogger(__name__)

_INTERVALS = {
    'hours': lambda interval: relativedelta(hours=interval),
    'days': lambda interval: relativedelta(days=interval),
    'weeks': lambda interval: relativedelta(days=7 * interval),
    'months': lambda interval: relativedelta(months=interval),
    'now': lambda interval: relativedelta(hours=0),
}


class EventMailScheduler(models.Model):
    _inherit = "event.mail"

    interval_type = fields.Selection(
        selection_add=[('open_event_slot', 'If there is a open spot on the event'),
                       ('mandatory_event_consule', 'If the precipitation is cancelled')],
        ondelete={'open_event_slot': 'set default', 'mandatory_event_consule': 'set default'})

    @api.depends('event_id.date_begin', 'event_id.date_end', 'interval_type', 'interval_unit', 'interval_nbr')
    def _compute_scheduled_date(self):
        for scheduler in self:
            if scheduler.interval_type == 'after_sub' or scheduler.interval_type == 'open_event_slot':
                date, sign = scheduler.event_id.create_date, 1
            elif scheduler.interval_type == 'before_event':
                date, sign = scheduler.event_id.date_begin, -1
            else:
                date, sign = scheduler.event_id.date_end, 1

            scheduler.scheduled_date = date.replace(microsecond=0) + _INTERVALS[scheduler.interval_unit](
                sign * scheduler.interval_nbr) if date else False

    @api.depends('interval_type', 'scheduled_date', 'mail_done')
    def _compute_mail_state(self):
        for scheduler in self:
            # registrations based
            if scheduler.interval_type == 'after_sub' or scheduler.interval_type == 'open_event_slot':
                scheduler.mail_state = 'running'
            # global event based
            elif scheduler.mail_done:
                scheduler.mail_state = 'sent'
            elif scheduler.scheduled_date:
                scheduler.mail_state = 'scheduled'
            else:
                scheduler.mail_state = 'running'

    def execute(self):
        for scheduler in self:
            now = fields.Datetime.now()
            if scheduler.interval_type == 'open_event_slot':
                waiting_list_ids = self.env['event.waiting.list'].search([
                    ('event_type_id', '=', scheduler.event_id.event_type_id.id)
                ])
                for event_wait_contact in waiting_list_ids:
                    #scheduler.event_id = scheduler.event_id
                    event_wait_contact.event_id = scheduler.event_id
                    self.env['mail.template'].browse(scheduler.template_ref.id).send_mail(event_wait_contact.id,
                                                                                          force_send=True)
                    event_wait_contact.event_id = False
                scheduler.update({
                    'mail_done': True,
                })

            elif scheduler.interval_type == 'after_sub':
                if self.env.context.get('event_mail_registration_ids'):
                    new_registrations = self.env['event.registration'].search([
                        ('id', 'in', self.env.context['event_mail_registration_ids']),
                        ('event_id', '=', scheduler.event_id.id),
                    ]) - scheduler.mail_registration_ids.registration_id
                else:
                    new_registrations = scheduler.event_id.registration_ids.filtered_domain(
                        [('state', 'not in', ('cancel', 'draft'))]
                    ) - scheduler.mail_registration_ids.registration_id
                scheduler._create_missing_mail_registrations(new_registrations)
                # execute scheduler on registrations
                scheduler.mail_registration_ids.execute()
                total_sent = len(scheduler.mail_registration_ids.filtered(lambda reg: reg.mail_sent))
                scheduler.update({
                    'mail_done': total_sent >= (scheduler.event_id.seats_reserved + scheduler.event_id.seats_used),
                    'mail_count_done': total_sent,
                })
            else:
                # before or after event -> one shot email
                if scheduler.mail_done or scheduler.notification_type != 'mail':
                    continue
                # no template -> ill configured, skip and avoid crash
                if not scheduler.template_ref:
                    continue
                # do not send emails if the mailing was scheduled before the event but the event is over
                if scheduler.scheduled_date <= now and (
                        scheduler.interval_type != 'before_event' or scheduler.event_id.date_end > now):
                    scheduler.event_id.mail_attendees(scheduler.template_ref.id)
                    # Mail is sent to all attendees (unconfirmed as well), so count all attendees
                    scheduler.update({
                        'mail_done': True,
                        'mail_count_done': len(
                            scheduler.event_id.registration_ids.filtered(lambda r: r.state != 'cancel'))
                    })
        return True
