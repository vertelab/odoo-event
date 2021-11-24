from odoo import models, fields, api, _


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    state = fields.Selection(selection_add=[('reservation', 'Reservation')])

