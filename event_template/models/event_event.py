from odoo import models, fields, api, _


class EventEvent(models.Model):
    _inherit = 'event.event'

    is_template = fields.Boolean(string="Is Template", copy=False)

    # CREATE A PROJECT FROM A TEMPLATE AND OPEN THE NEWLY CREATED PROJECT
    def create_event_from_template(self):
        if " (TEMPLATE)" in self.name:
            new_name = self.name.replace(" (TEMPLATE)", " (COPY)")
        else:
            new_name = self.name + " (COPY)"
        new_event = self.copy(
            default={"name": new_name, "active": True}
        )

        # OPEN THE NEWLY CREATED PROJECT FORM
        return {
            "view_type": "form",
            "view_mode": "form",
            "res_model": "event.event",
            "target": "current",
            "res_id": new_event.id,
            "type": "ir.actions.act_window",
        }

    # ADD "(TEMPLATE)" TO THE NAME WHEN PROJECT IS MARKED AS A TEMPLATE
    @api.onchange("is_template")
    def on_change_is_template(self):
        # Add "(TEMPLATE)" to the Name if is_template == true
        if self.name:
            if self.is_template:
                if "(TEMPLATE)" not in self.name:
                    self.name = self.name + " (TEMPLATE)"
            else:
                if " (TEMPLATE)" in self.name:
                    self.name = self.name.replace(" (TEMPLATE)", "")
