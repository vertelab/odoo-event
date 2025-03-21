from odoo import models, fields, api, _
from odoo.tools import slug

import logging

class EventEvent(models.Model):

	_inherit = 'event.event'

	is_waitinglist = fields.Boolean(string='Is Waiting List')





