from odoo import models, fields, api, _
from odoo.tools.translate import html_translate
import logging
_logger = logging.getLogger(__name__)

class EventEventType(models.Model):
        _inherit = 'event.type'
        
        def _default_description(self):
            return self.env['ir.ui.view']._render_template('event.event_default_descripton')
            
        description = fields.Html(string='Description', translate=html_translate, sanitize_attributes=False, sanitize_form=False, default=_default_description)
        ticket_description = fields.Text(default="There is no description", compute='_set_default_ticket_description')
        
        @api.onchange("event_type_ticket_ids")
        def _set_default_ticket_description(self):
            _logger.warning(f"{self.description=}")
            if self.event_type_ticket_ids:
                self.ticket_description = self.event_type_ticket_ids[0].product_id.description_sale
            else:
                self.ticket_description = ""


class EventEvent(models.Model):
        _inherit = 'event.event'
        
        ticket_description= fields.Text(default="There is no description", compute='_set_default_ticket_description')
        
        @api.onchange("event_type_id")
        def _set_decription_to_event_type_description(self):
            self.description = self.event_type_id.description


        @api.onchange("event_ticket_ids")
        def _set_default_ticket_description(self):
            if self.event_ticket_ids:
                self.ticket_description = self.event_ticket_ids[0].product_id.description_sale
            else:
                self.ticket_description = ""