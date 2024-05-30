import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class EventRegistration(models.Model):
    _inherit = 'event.registration'
    slide_channel_partner_id = fields.Many2one(
        string="Event Registration", comodel_name="slide.channel.partner",
    )
    
    hr_employee_manager_id = fields.Many2one(
        string="Employee", comodel_name="hr.employee", compute='_compute_hr_employee_manager_id', readonly=False, store=True)

    @api.depends('hr_employee_manager_id')
    def _compute_hr_employee_manager_id(self):
        
        for registration in self:

            registration.hr_employee_manager_id = False

            hr_employee_domain = [('name', '=', registration.name),('work_phone', '=', registration.phone),('work_email', '=', registration.email)]
            
            hr_employee_id = self.env['hr.employee'].search(hr_employee_domain)
            
            if hr_employee_id:

                registration.hr_employee_manager_id = hr_employee_id.parent_id


    def action_cancel(self):
        
        res = super().action_cancel()
        
        ## Hitta rätt mail scedular och lägga in event.mail.registration classen på den.
        mail_schedulers = self.env['event.mail'].search([('event_id','=',self.event_id.id),('interval_type','=','after_cancel')])
        
        for mail_scheduler in mail_schedulers:

            registrations_not_yet_in_scheduler_domain = [('id', 'in', self.ids),('event_id', '=', mail_scheduler.event_id.id)]

            registrations_not_yet_in_scheduler = self.env['event.registration'].search(registrations_not_yet_in_scheduler_domain)

            for mail_registration in mail_scheduler.mail_registration_ids:

                if mail_registration.registration_id in registrations_not_yet_in_scheduler:

                    mail_registration.mail_sent = False

            new_canceled_registrations = registrations_not_yet_in_scheduler - mail_scheduler.mail_registration_ids.registration_id

            mail_scheduler._create_missing_mail_registrations(new_canceled_registrations)

            all_mail_done = all(mail_registration.mail_sent == True for mail_registration in mail_scheduler.mail_registration_ids)
            total_sent = len(mail_scheduler.mail_registration_ids.filtered(lambda reg: reg.mail_sent))

            mail_scheduler.update({
                    'mail_done': all_mail_done,
                    'mail_count_done': total_sent
                })

        _logger.warning("cancel was invoked!!!!!"*100)

        return res

    def writeSlideChannelPartner(self):
        for record in self:
            if record.state == "open" and record.event_id.slide_channel_id and not record.slide_channel_partner_id:
               partner_id = self.env['res.partner'].search([('name','=',record.name),('phone','=',record.phone),('email','=',record.email),('user_ids','!=',False),('employee_ids','!=',False)], limit=1)
               if not partner_id:
                   partner_id = self.env['res.partner'].search([('name','=',record.name),('phone','=',record.phone),('email','=',record.email),('user_ids','!=',False)], limit=1)
               if not partner_id:
                   partner_id = self.env['res.partner'].search([('name','=',record.name),('phone','=',record.phone),('email','=',record.email)], limit=1)
               if not partner_id:
                   partner_id = self.env['res.partner'].search([('name','=',record.name),('email','=',record.email)], limit=1)
               if not partner_id:
                   partner_id = self.env['res.partner'].search([('email','=',record.email)], limit=1)
               if not partner_id:
                   partner_id = self.env['res.partner'].create({
                   'name':record.name,
                   'phone':record.phone,
                   'email':record.email,
                   })
               slide_channel_partner_id = record.env['slide.channel.partner'].search([('channel_id','=',record.event_id.slide_channel_id.id),('partner_id','=',partner_id.id),('event_registration_ids','=',record.id)])
               logging.warning(f"{slide_channel_partner_id=}")
               slide_channel_partner_id = record.env['slide.channel.partner'].search([('channel_id','=',record.event_id.slide_channel_id.id),('partner_id','=',partner_id.id)])
               logging.warning(f"{slide_channel_partner_id=}")
               logging.warning(f"{slide_channel_partner_id.event_registration_ids=}")
               
               if not slide_channel_partner_id:
                   slide_channel_partner_id = record.env['slide.channel.partner'].create({
                   'channel_id':record.event_id.slide_channel_id.id,
                   'partner_id':partner_id.id,
                   # ~ 'event_registration_id':record.id,
                   })
               record.slide_channel_partner_id = slide_channel_partner_id

    @api.model
    def createSlideChannelPartner(self, vals_list):
        
        for vals in vals_list:
            logging.warning(f"{vals=}")
            event_id = self.env['event.event'].browse(vals.get('event_id'))
            logging.warning(f"{vals.get('event_id')=}")
            if vals.get('state','open') == "open" and event_id.slide_channel_id:
               logging.warning(f"IF CASE COMPLetete")
               partner_id = self.env['res.partner'].search([('name','=',vals.get('name')),('phone','=',vals.get('phone')),('email','=',vals.get('email')),('user_ids','!=',False),('employee_ids','!=',False)], limit=1)
               if not partner_id:
                   partner_id = self.env['res.partner'].search([('name','=',vals.get('name')),('phone','=',vals.get('phone')),('email','=',vals.get('email')),('user_ids','!=',False)], limit=1)
               if not partner_id:
                   partner_id = self.env['res.partner'].search([('name','=',vals.get('name')),('phone','=',vals.get('phone')),('email','=',vals.get('email'))], limit=1)
               if not partner_id:
                   partner_id = self.env['res.partner'].search([('name','=',vals.get('name')),('email','=',vals.get('email'))], limit=1)
               if not partner_id:
                   partner_id = self.env['res.partner'].search([('email','=',vals.get('email'))], limit=1)
               if not partner_id:
                   partner_id = self.env['res.partner'].create({
                   'name':vals.get('name'),
                   'phone':vals.get('phone'),
                   'email':vals.get('email'),
                   })

               slide_channel_partner_id = self.env['slide.channel.partner'].search([('channel_id','=',event_id.slide_channel_id.id),('partner_id','=',partner_id.id)])
               if not slide_channel_partner_id:
                   slide_channel_partner_id = self.env['slide.channel.partner'].create({
                   'channel_id':event_id.slide_channel_id.id,
                   'partner_id':partner_id.id,
                   })
               vals['slide_channel_partner_id'] = slide_channel_partner_id.id
        return vals_list
    
    def write(self, vals):
        res = super(EventRegistration, self).write(vals)
        if 'state' in vals and vals['state'] == "open":
            logging.warning(f'{vals=}')
            if self.event_id.slide_channel_id and not self.slide_channel_partner_id:
               self.writeSlideChannelPartner()
        return res


    @api.model_create_multi
    def create(self, vals_list):
        vals_list = self.createSlideChannelPartner(vals_list)
        registrations = super(EventRegistration, self).create(vals_list)
        return registrations


