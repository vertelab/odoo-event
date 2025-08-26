import logging
from odoo import models, fields, api, _

_logger = logging.getLogger(__name__)


class EventRegistration(models.Model):
    _inherit = 'event.registration'
    slide_channel_partner_id = fields.Many2one(
        string="Event Registration", comodel_name="slide.channel.partner",
    )
    
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
               slide_channel_partner_id = record.env['slide.channel.partner'].search([('channel_id','=',record.event_id.slide_channel_id.id),('partner_id','=',partner_id.id),'|',('active','=',True),('active','=',False)])
               logging.warning(f"{slide_channel_partner_id=}")
               logging.warning(f"{slide_channel_partner_id.event_registration_ids=}")
               
               if not slide_channel_partner_id:
                   slide_channel_partner_id = record.env['slide.channel.partner'].create({
                   'channel_id':record.event_id.slide_channel_id.id,
                   'partner_id':partner_id.id,
                   # ~ 'event_registration_id':record.id,
                   })
               slide_channel_partner_id.active = True
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


