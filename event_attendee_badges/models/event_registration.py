# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import requests
from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class event_registration(models.Model):
    _inherit = 'event.registration'
    
    attendee_company_name = fields.Text(string="Attendee Company Name", default="              \n")
    
    @api.onchange('partner_id')
    def set_company_name(self):
        for record in self:
            if record.partner_id.commercial_company_name:
                record.attendee_company_name = record.partner_id.commercial_company_name
            else:
                record.partner_id.commercial_company_name = "              \n"
                
