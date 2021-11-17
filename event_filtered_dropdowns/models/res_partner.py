# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pytz

from odoo import _, api, fields, models
from odoo.addons.base.models.res_partner import _tz_get
from odoo.tools import format_datetime
from odoo.exceptions import ValidationError
from odoo.tools.translate import html_translate

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    """Event"""
    _inherit = 'res.partner'

    type = fields.Selection(selection_add=[('hr_department', 'Department')])
