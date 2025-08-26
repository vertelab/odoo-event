# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
import binascii

from odoo import _, api, exceptions, fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    auto_confirm_reserved = fields.Boolean('Auto Confirm Reserved',
        config_parameter='event_reservation.auto_confirm_reserved', readonly=False)

