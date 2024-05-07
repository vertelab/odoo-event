# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, _


class EventRegistration(models.Model):
    _inherit = "event.registration"

    partner_gender = fields.Selection(
        string="Partner gender",
        selection=[
            ("male", _("Male")),
            ("female", _("Female")),
            ("other", _("Other")),
            ("decline", _("Decline to answer")),
        ],
        readonly=True,
    )

    def _get_website_registration_allowed_fields(self):
        res = super(EventRegistration, self)._get_website_registration_allowed_fields()
        res.add('partner_gender')
        return res

    def _query(self, with_clause="", fields={}, groupby="", from_clause=""):
        fields["partner_gender"] = ", partner.gender as partner_gender"
        groupby += ", partner.gender"
        return super()._query(with_clause, fields, groupby, from_clause)
