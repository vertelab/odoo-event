from odoo import models, fields, api, _


class EventEvent(models.Model):
    _inherit = 'event.event'

    # Explicit relation table: OCA/event_contact defines ``contact_ids`` on the
    # same model with the same comodel, which would otherwise collide on the
    # auto-generated table (event_event_res_partner_rel).
    res_partner_ids = fields.Many2many(
        'res.partner',
        'event_event_res_partner_ids_rel',
        'event_id',
        'partner_id',
        string="Partners",
    )
