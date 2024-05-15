from odoo import models, fields

class EventType(models.Model):
    
    _inherit = 'event.type'

    slide_channel_id = fields.Many2one(
        string="Slide Channel", comodel_name="slide.channel",
    )

    def _default_event_mail_type_ids(self):
        return [(0, 0,
                 {'notification_type': 'mail',
                  'interval_nbr': 0,
                  'interval_unit': 'now',
                  'interval_type': 'after_sub',
                  'template_ref': 'mail.template, %i' % self.env.ref('event_elearning.event_subscription_with_slide_link').id,
                 }),
                (0, 0,
                 {'notification_type': 'mail',
                  'interval_nbr': 1,
                  'interval_unit': 'hours',
                  'interval_type': 'before_event',
                  'template_ref': 'mail.template, %i' % self.env.ref('event_elearning.event_reminder_with_slide_link').id,
                 }),
                (0, 0,
                 {'notification_type': 'mail',
                  'interval_nbr': 3,
                  'interval_unit': 'days',
                  'interval_type': 'before_event',
                  'template_ref': 'mail.template, %i' % self.env.ref('event_elearning.event_reminder_with_slide_link').id,
                 })]
