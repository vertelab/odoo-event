from odoo import fields, models, _

class EventEvent(models.Model):
    _inherit = "event.event"
    food_is_served = fields.Boolean(default = False)

class EventRegistration(models.Model):
    _inherit = "event.registration"
    food_allergy = fields.Char(string=_("Food allergy"))
    food_is_served = fields.Boolean(related = "event_id.food_is_served")

    def _get_website_registration_allowed_fields(self):
        res = super(EventRegistration,self)._get_website_registration_allowed_fields()
        res.add('food_allergy')
        return res
