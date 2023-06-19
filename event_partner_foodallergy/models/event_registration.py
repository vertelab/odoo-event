from odoo import fields, models, _

class EventEvent(models.Model):
    _inherit = "event.event"
    food_is_served = fields.Boolean(default = False)

class EventRegistration(models.Model):
    _inherit = "event.registration"
    food_allergy = fields.Char(string=_("Food allergy"))
    special_food = fields.Boolean(string=_('Special food'), compute="_has_food_allergy", readonly=True)
    food_is_served = fields.Boolean(related = "event_id.food_is_served")

    def _get_website_registration_allowed_fields(self):
        res = super(EventRegistration,self)._get_website_registration_allowed_fields()
        res.add('food_allergy')
        return res

    def _has_food_allergy(self):
        if self.food_allergy:
            if len(self.food_allergy) > 0:
                self.special_food = True
            else:
                self.special_food = False
        else:
            self.special_food = False
