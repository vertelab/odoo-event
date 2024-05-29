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

        res = super()._compute_scheduled_date()

        for scheduler in self:
            if scheduler.interval_type == 'after_cancel':
                date, sign = scheduler.event_id.create_date, 1

                scheduler.scheduled_date = date.replace(microsecond=0) + _INTERVALS[scheduler.interval_unit](sign * scheduler.interval_nbr) if date else False

        return res
    

    @api.depends('interval_type', 'scheduled_date', 'mail_done')
    def _compute_mail_state(self):
        
        res = super()._compute_mail_state()
        
        for scheduler in self:
            # registrations based
            if scheduler.interval_type == 'after_cancel':
                scheduler.mail_state = 'running'

        return res


    def _filter_schedulers(self,scheduler):

        if scheduler.interval_type == 'after_cancel':

            return scheduler
        

    def execute(self):

        for scheduler in self:
            
            if scheduler.interval_type == 'after_cancel':
                
                _logger.error(100*"cancel mail!!!!")

                for mail_registration in scheduler.mail_registration_ids:

                    registration = mail_registration.registration_id

                    if mail_registration.mail_sent == False:

                        if registration.hr_employee_manager_id:
                            
                            self.env['mail.template'].browse(scheduler.template_ref.id).send_mail(registration.id, force_send=True)
                    
                        mail_registration.mail_sent = True
                        
                all_mail_done = all(mail_registration.mail_sent == True for mail_registration in scheduler.mail_registration_ids)
                total_sent = len(scheduler.mail_registration_ids.filtered(lambda reg: reg.mail_sent))

                scheduler.update({
                    'mail_done': all_mail_done,
                    'mail_count_done': total_sent
                })

            schedulers = scheduler.filtered(lambda s: s.interval_type != 'after_cancel')
            return super(EventMailScheduler, schedulers).execute()