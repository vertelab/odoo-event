from odoo import models, fields, api, _
import logging
class EventType(models.Model):
    _inherit = 'event.type'
    slide_channel_id = fields.Many2one(
        string="Slide Channel", comodel_name="slide.channel",
    )
    

class Event(models.Model):
    _inherit = 'event.event'

    slide_channel_id = fields.Many2one(
        string="Slide Channel", comodel_name="slide.channel", compute='_compute_slide_channel', precompute=True, readonly=False, store=True)
    
    
    @api.depends('event_type_id')
    def _compute_slide_channel(self):
        for event in self:
            if event.event_type_id.slide_channel_id:
                event.slide_channel_id = event.event_type_id.slide_channel_id

    
class SlideChannel(models.Model):
    _inherit = 'slide.channel'
    event_event_ids = fields.One2many('event.event', 'slide_channel_id', 'Events')


class EventRegistration(models.Model):
    _inherit = 'event.registration'
    slide_channel_partner_id = fields.Many2one(
        string="Event Registration", comodel_name="slide.channel.partner",
    )
    
    def createSlideChannelPartner(self):
        logging.warning("create_slideChannelPartner"*100)
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
    
    def write(self, vals):
        logging.warning("event write"*100)        
        res = super(EventRegistration, self).write(vals)
        if 'state' in vals and vals['state'] == "open":
            logging.warning(f'{vals=}')
            if self.event_id.slide_channel_id and not self.slide_channel_partner_id:
               self.createSlideChannelPartner()
        return res
    
    @api.model_create_multi
    def create(self, vals_list):
        registrations = super(EventRegistration, self).create(vals_list)
        registrations.createSlideChannelPartner()
        return registrations

class SlideChannelPartner(models.Model):
    _inherit = 'slide.channel.partner'
    event_registration_ids = fields.One2many('event.registration', 'slide_channel_partner_id', 'Events Registrations')


