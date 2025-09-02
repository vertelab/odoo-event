from odoo import models, fields, api, _

class SlideChannel(models.Model):
    _inherit = 'slide.channel'

    event_event_ids = fields.One2many('event.event', 'slide_channel_id', 'Events')
    nbr_event_type = fields.Integer("Number of Teacher-led opportunitys", compute='_compute_slides_statistics', store=True)
    

class SlideSlide(models.Model):
    _inherit = 'slide.slide'

    slide_category = fields.Selection(selection_add=[('event_type',"Teacher-led opportunity")], ondelete={"event_type": "set default"})
    event_type_id = fields.Many2one('event.type','Teacher-led opportunity type')
    nbr_event_type = fields.Integer("Number of Teacher-led opportunitys", compute='_compute_slides_statistics', store=True)



    

    
