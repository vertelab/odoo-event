# Copyright 2019 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, modules, _

import logging
_logger = logging.getLogger(__name__)


class Users(models.Model):
    _inherit = "res.users"

    @api.model
    def review_user_count(self):
        res = super(Users, self).review_user_count()
        _logger.error(f'RES IS: {res}');
        return res;