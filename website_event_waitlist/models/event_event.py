from odoo import models, fields, api, _
# ~ from odoo.tools import slug
# ~ from odoo.addons.http_routing.models.ir_http import slug


import re

def slug(value):
    value = str(value)
    value = value.lower()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    value = value.strip('-')
    return value



import logging

class EventEvent(models.Model):

	_inherit = 'event.event'

	is_waitinglist = fields.Boolean(string='Is Waiting List')





