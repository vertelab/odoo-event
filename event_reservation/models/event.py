from odoo import models, fields, api, _
import logging

class EventRegistration(models.Model):
    _inherit = 'event.registration'

    state = fields.Selection(selection_add=[('reservation', 'Reservation')])

    def _confirm_next_reservation(self):
        auto_confirm_reserved = self.env['ir.config_parameter'].sudo().get_param(
            'event_reservation.auto_confirm_reserved'
        )
        for record in self:
            if record.state == 'cancel' and auto_confirm_reserved:
                if record.event_id.seats_limited and record.event_id.seats_available > 0 and record.event_id.seats_used < record.event_id.seats_max:
                    next_candidate = record._get_oldest_reservation_for_event()
                    if next_candidate:
                       next_candidate.action_confirm()
                       next_candidate._send_confirmation_notification()

    def _send_confirmation_notification(self):
        """
        Send notification to participant when confirmed from reservation
        """
        template = self.env.ref('event.event_registration_mail_template_badge', raise_if_not_found=False)
        email_vals = {'subject': 'Congratulations, Your Spot has been Confirmed!!!'}
        if template:
            template.send_mail(self.id, email_values=email_vals, force_send=True)

    def _get_oldest_reservation_for_event(self):
        return self.env['event.registration'].search([
            ('state', '=', 'reservation'),
            ('event_id', '=', self.event_id.id)
        ], order='create_date asc', limit=1)


    def action_cancel(self):
        if self.state in ['open', 'done']:
            result = super().action_cancel()
            self._confirm_next_reservation()
            return result
        return super().action_cancel()
    
    def unlink(self):
        self._confirm_next_reservation()
        return super().unlink()



class EventReservationTicket(models.Model):
    _inherit = 'event.event.ticket'

    seats_available_event_limit = fields.Integer(string='Available Seats Event Limit',
                                                 compute='_compute_seats_event_limit', store=True)

    @api.depends('seats_max', 'registration_ids.state', 'event_id', 'event_id.seats_limited', 'event_id.seats_max',
                 'event_id.seats_available')
    def _compute_seats_event_limit(self):
        #TODO figure out the purpose of this module and fix compute
        #self.seats_available_event_limit = False
        #return
        """ Determine reserved, available, reserved but unconfirmed and used seats. """
        # initialize fields to 0 + compute seats availability
        for ticket in self:
            #ticket.seats_unconfirmed = ticket.seats_reserved = ticket.seats_used = ticket.seats_available = 0
            ticket.seats_reserved = ticket.seats_used = ticket.seats_available = 0
        # aggregate registrations by ticket and by state
        results = {}
        if self.ids:
            state_field = {
            'open': 'seats_reserved',
            'done': 'seats_used',
            }

            query = """ SELECT event_ticket_id, state, count(event_id)
                        FROM event_registration
                        WHERE event_ticket_id IN %s AND state IN ('open', 'done')
                        GROUP BY event_ticket_id, state
                    """
            self.env['event.registration'].flush_model(['event_id', 'event_ticket_id', 'state'])
            self.env.cr.execute(query, (tuple(self.ids),))
            for event_ticket_id, state, num in self.env.cr.fetchall():
                results.setdefault(event_ticket_id, {})[state_field[state]] = num

        # compute seats_available
        for ticket in self:
            ticket.update(results.get(ticket._origin.id or ticket.id, {}))
            if ticket.seats_max > 0:
                ticket.seats_available = ticket.seats_max - (ticket.seats_reserved + ticket.seats_used)
                if ticket.event_id and ticket.event_id.seats_limited:
                    ticket.seats_available_event_limit = min(ticket.seats_available, ticket.event_id.seats_available)
                else:
                    ticket.seats_available_event_limit = ticket.seats_available
            elif ticket.event_id.seats_limited:
                ticket.seats_available_event_limit = ticket.event_id.seats_available
            else:
                ticket.seats_available_event_limit = 0


class EventEvent(models.Model):
    _inherit = 'event.event'

    def mail_attendees(self, template_id, force_send=False, filter_func=lambda self: self.state not in ('cancel', 'draft', 'reservation')):
        for event in self:
            for attendee in event.registration_ids.filtered(filter_func):
                self.env['mail.template'].browse(template_id).send_mail(attendee.id, force_send=force_send)
