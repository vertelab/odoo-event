from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)


class EventEvent(models.Model):
        _inherit = 'event.event'
        
        is_waitinglist = fields.Boolean(string='Is Waiting List')
        
        
        


