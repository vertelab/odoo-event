from odoo import models, fields, api, _

class EventTypeMail(models.Model):

    _inherit = 'event.type.mail'

    interval_type = fields.Selection(
        selection_add=[('open_event_slot','If there is a event based on the same templet')], 
        ondelete={'open_event_slot': 'set default'})