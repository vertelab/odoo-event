# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from email.policy import default
from odoo import fields, models, _


class EventEvent(models.Model):
    _name = "event.event"
    _inherit = ["event.event", 'mail.activity.mixin', 'mail.thread']

