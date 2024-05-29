from odoo import models, fields, api, _

class EventTypeMail(models.Model):

    _inherit = 'event.type.mail'

    interval_type = fields.Selection(
        selection_add=[('after_cancel','If the registration is cancelled')], 
        ondelete={'after_cancel': 'set default'})