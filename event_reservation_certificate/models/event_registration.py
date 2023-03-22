# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from email.policy import default
from odoo import fields, models, _


class EventRegistration(models.Model):
    _inherit = "event.registration"

    certified = fields.Selection(selection=[
        ('True', 'Approved'),
        ('False', 'Unapproved'),
    ], default='False',)

    def action_certify(self):
        self.certified = 'True'
    