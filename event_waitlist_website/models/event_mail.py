import logging
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import MissingError, ValidationError


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
        selection_add=[('open_event_slot','If there is a event based on the same templet')], 
        ondelete={'open_event_slot': 'set default'})
    

    @api.depends('event_id.date_begin', 'event_id.date_end', 'interval_type', 'interval_unit', 'interval_nbr')
    def _compute_scheduled_date(self):
        
        res = super()._compute_scheduled_date()
        for scheduler in self:
            if scheduler.interval_type == 'open_event_slot':
                date, sign = scheduler.event_id.create_date, 1
                scheduler.scheduled_date = date.replace(microsecond=0) + _INTERVALS[scheduler.interval_unit](sign * scheduler.interval_nbr) if date else False

        return res

    @api.depends('interval_type', 'scheduled_date', 'mail_done')
    def _compute_mail_state(self):

        res = super()._compute_mail_state()

        for scheduler in self:
            # registrations based
            if scheduler.interval_type == 'open_event_slot':
                scheduler.mail_state = 'running'

        return res


    def execute(self):
        
        for scheduler in self:

            if scheduler.interval_type == 'open_event_slot':
               
                waiting_list_ids = self.env['event.waiting.list'].search([
                    ('event_type_id','=',scheduler.event_id.event_type_id.id)
                ])
                    
                for waiting_list_id in waiting_list_ids:

                    waiting_list_id.event_id = scheduler.event_id

                    self.env['mail.template'].browse(scheduler.template_ref.id).send_mail(waiting_list_id.id, force_send=True)

                    waiting_list_id.event_id = False


                all_mail_done = True

                scheduler.update({
                    'mail_done': all_mail_done,
                })
        
            schedulers = scheduler.filtered(lambda s: s.interval_type != 'open_event_slot')
            return super(EventMailScheduler, schedulers).execute()
    