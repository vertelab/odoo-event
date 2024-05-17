import logging
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta

_logger = logging.getLogger(__name__)

_INTERVALS = {
    'hours': lambda interval: relativedelta(hours=interval),
    'days': lambda interval: relativedelta(days=interval),
    'weeks': lambda interval: relativedelta(days=7*interval),
    'months': lambda interval: relativedelta(months=interval),
    'now': lambda interval: relativedelta(hours=0),
}

class EventMailScheduler(models.Model):

    _inherit = "event.mail"

    interval_type = fields.Selection(
        selection_add=[('after_cancel','If the registration is cancelled')], 
        ondelete={'after_cancel': 'set default'})

    @api.depends('event_id.date_begin', 'event_id.date_end', 'interval_type', 'interval_unit', 'interval_nbr')
    def _compute_scheduled_date(self):
        for scheduler in self:
            if scheduler.interval_type == 'after_sub' or scheduler.interval_type == 'open_event_slot' or scheduler.interval_type == 'after_cancel':
                date, sign = scheduler.event_id.create_date, 1
            elif scheduler.interval_type == 'before_event':
                date, sign = scheduler.event_id.date_begin, -1
            else:
                date, sign = scheduler.event_id.date_end, 1

            scheduler.scheduled_date = date.replace(microsecond=0) + _INTERVALS[scheduler.interval_unit](sign * scheduler.interval_nbr) if date else False


    @api.model
    def schedule_communications(self, autocommit=False):
                
        schedulers = self.search([
            ('event_id.active', '=', True),
            ('mail_done', '=', False),
            ('scheduled_date', '<=', fields.Datetime.now())
        ])

        for scheduler in schedulers:
            try:
                # Prevent a mega prefetch of the registration ids of all the events of all the schedulers
                self.browse(scheduler.id).after_cancel_exacute()
            except Exception as e:
                _logger.exception(e)
                self.env.invalidate_all()
                self._warn_template_error(scheduler, e)


        super().schedule_communications()


    def after_cancel_exacute(self):

        for scheduler in self:
            
            if scheduler.interval_type == 'after_cancel':

                attendee_ids = self.env['event.registration'].search([
                    ('event_type_id','=',scheduler.event_id.event_type_id.id)
                ])

                for attendee in attendee_ids:
                    attendee.event_id = scheduler.event_id
                    self.env['mail.template'].browse(scheduler.template_ref.id).send_mail(attendee.id, force_send=True)
                    attendee.event_id = False
                
                scheduler.update({
                    'mail_done': True,
                })