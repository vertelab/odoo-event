# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class EventRegistration(models.Model):
    _inherit = 'event.registration'
    
    attendee_company_name = fields.Char(
        string="Attendee Company Name", related="partner_id.commercial_company_name"
    )
    attendee_company_image = fields.Image(
        string="Attendee Company Image", related="partner_id.commercial_partner_id.image_1920",
    )




