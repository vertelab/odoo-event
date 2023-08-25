# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
import logging
_logger = logging.getLogger(__name__)

class Event_event(models.Model):
    _inherit = 'event.event'
    calendar_event_id = fields.Many2one('calendar.event',readonly=True)

    # create_event re-creates the event as a meeting in the calendar
    def create_event(self):
        for rec in self:
            if rec.calendar_event_id and rec.date_begin:
                rec.calendar_event_id.write({'start': rec.date_begin, 'stop': rec.date_end})
            elif rec.date_begin:
                rec.calendar_event_id = rec.env['calendar.event'].with_context(no_mail_to_attendees=True).create({
                            'name': rec.name,
                            'description': _('Planned event'),
                            'start': rec.date_begin,
                            'stop': rec.date_end,
                            'privacy': 'confidential',
                        })

    @api.model
    def create(self,vals):
        res = super(Event_event, self).create(vals)
        if vals.get('date_begin'):
            res.create_event()
        return res

    def write(self,values):
        res = super(Event_event,self).write(values)
        if values.get('date_begin') or values.get('date_end'):
            self.create_event()
        return res

    # Unlinks the calendar meeting if the event is removed
    def unlink(self):
        self.calendar_event_id.unlink()
        for rec in self:
            for event_reg in rec.env['event.registration'].search([('event_id','=',rec.id)]):
               event_reg.unlink()   # unlinks registrations (attendees) from the event before it's unlinked
        res = super(Event_event,self).unlink()

    # get_attendees returns a new list of attendees from partner_id and re-adds the person who created the event
    def get_attendees(self):
        for rec in self:
            registrations = rec.env['event.registration'].search([('event_id','=',rec.id),('state','!=','cancel')])
            attendee_list = []
            for attendee in registrations:
                if attendee.partner_id:
                    attendee_list.append(attendee.partner_id.id)
                if attendee.attendee_partner_id:
                    attendee_list.append(attendee.attendee_partner_id.id)
            arranger_id = rec.user_id and rec.user_id.partner_id.id or False
            if arranger_id:
                attendee_list.append(arranger_id)
            return attendee_list

class Event_reg(models.Model):
    _inherit = 'event.registration'

    @api.model
    def create(self,vals):
        res = super(Event_reg, self).create(vals)
        self.update_event_attendees()
        return res

    def write(self,vals):
        res = super().write(vals)
        self.update_event_attendees()
        return res
    
    def unlink(self):
        _logger.warning(f"{self.event_id=}")
        self.update_event_attendees()
        res = super().unlink()
        return res

    # Updates the calendar when attendees are added/removed from the event
    def update_event_attendees(self):
        for res in self:
            if res.event_id.id:
                event = res.env['event.event'].search([('id','=',res.event_id.id)])
                attendees = event.get_attendees()
                if attendees:
                    event.calendar_event_id.write({'partner_ids':[(6, 0, attendees)]})
