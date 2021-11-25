from odoo import models, fields, api, _
from odoo.tools.translate import html_translate
import logging
_logger = logging.getLogger(__name__)
from odoo.addons.http_routing.models.ir_http import slug

class EventEventType(models.Model):
        _inherit = 'event.type'
        
        def _default_description(self):
            return self.env['ir.ui.view']._render_template('event.event_default_descripton')
            
        description = fields.Html(string='Description', translate=html_translate, sanitize_attributes=False, sanitize_form=False, default=_default_description)
        ticket_description = fields.Text(default="There is no description", compute='_set_default_ticket_description')
        
        @api.onchange("event_type_ticket_ids")
        def _set_default_ticket_description(self):
            self.ticket_description = ""
            _logger.warning(f"{self.description=}")
            if 'product_id' in self.env['event.event.ticket']._fields:
                if self.event_type_ticket_ids and self.event_ticket_ids[0].product_id:
                    self.ticket_description = self.event_type_ticket_ids[0].product_id.description_sale


class EventEvent(models.Model):
        _inherit = 'event.event'
        
        ticket_description= fields.Text(default="There is no description", compute='_set_default_ticket_description')
        
        #def _default_empty_description(self):
            #return self.env['ir.ui.view']._render_template('event_default_empty_description')
        #empty_description= fields.Text(default="   \n   \n   \n   \n    \n   \n   \n   \n    \n   \n   \n   \n    \n   \n   \n   \n    \n   \n   \n   \n    \n   \n   \n   \n", string="Is used for the description view since we want it to be empty, and if I remove it the formating breaks,so we have this useless empty string, go team!")
        empty_description_html = fields.Html(string='Description', translate=html_translate, sanitize_attributes=False, sanitize_form=False)
        
        @api.onchange("event_type_id")
        def _set_decription_to_event_type_description(self):
            self.description = self.event_type_id.description


        @api.onchange("event_ticket_ids")
        def _set_default_ticket_description(self):
            self.ticket_description = ""
            if 'product_id' in self.env['event.event.ticket']._fields:
                if self.event_ticket_ids and self.event_ticket_ids[0].product_id:
                    self.ticket_description = self.event_ticket_ids[0].product_id.description_sale
        
        


