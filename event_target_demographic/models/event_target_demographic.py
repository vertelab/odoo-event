from odoo import models, fields, api


class EventTargetDemographic(models.Model):
    _name = "event.target.demographic"
    _description = "Event Target Demographic"

    name = fields.Char()
    model_id = fields.Many2one('ir.model', string='Model', domain=[('transient', '=', False)])
    model_name = fields.Char(related='model_id.model', string='Model Name', readonly=True, store=True)
    domain = fields.Char(default="[]", help="Domain")
    user_ids = fields.Many2many('res.users', store=True)

    @api.onchange('model_id','domain')
    def compute_users(self):
        for record in self:
            record.user_ids = [(6, 0, self.env['res.users'].search(eval(record.domain)).ids)]
