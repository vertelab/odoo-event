from odoo import models, fields


class UIMenu(models.Model):
    _inherit = 'ir.ui.menu'

    def update_elearning_group(self):
        self.write({
            'groups_id': [(6, 0, [self.env.ref('event_lms.group_lms_elearning_admin_lms').id])]
        })
