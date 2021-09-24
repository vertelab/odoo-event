# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


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
                attendee_list.append(attendee.partner_id.id)
            arranger_id = rec.user_id.partner_id.id
            attendee_list.append(arranger_id)
            return attendee_list

class Event_reg(models.Model):
    _inherit = 'event.registration'

    # Updates the calendar when attendees are added/removed from the event
    @api.model
    def create(self,vals):
        res = super(Event_reg, self).create(vals)
        event = res.env['event.event'].search([('id','=',res.event_id.id)])
        event.calendar_event_id.write({'partner_ids':[(6, 0, event.get_attendees())]})
        return res
