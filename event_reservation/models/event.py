from odoo import models, fields, api, _


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    state = fields.Selection(selection_add=[('reservation', 'Reservation')])

class EventReservationTicket(models.Model):
    _inherit = 'event.event.ticket'
    seats_available_event_limit = fields.Integer(string='Available Seats Event Limit', compute='_compute_seats_event_limit', store=True)

    @api.depends('seats_max', 'registration_ids.state','event_id','event_id.seats_limited','event_id.seats_max')
    def _compute_seats_event_limit(self):
        """ Determine reserved, available, reserved but unconfirmed and used seats. """
        # initialize fields to 0 + compute seats availability
        for ticket in self:
            ticket.seats_unconfirmed = ticket.seats_reserved = ticket.seats_used = ticket.seats_available = 0
        # aggregate registrations by ticket and by state
        results = {}
        if self.ids:
            state_field = {
                'draft': 'seats_unconfirmed',
                'open': 'seats_reserved',
                'done': 'seats_used',
            }
            query = """ SELECT event_ticket_id, state, count(event_id)
                        FROM event_registration
                        WHERE event_ticket_id IN %s AND state IN ('draft', 'open', 'done')
                        GROUP BY event_ticket_id, state
                    """
            self.env['event.registration'].flush(['event_id', 'event_ticket_id', 'state'])
            self.env.cr.execute(query, (tuple(self.ids),))
            for event_ticket_id, state, num in self.env.cr.fetchall():
                results.setdefault(event_ticket_id, {})[state_field[state]] = num

        # compute seats_available
        for ticket in self:
            ticket.update(results.get(ticket._origin.id or ticket.id, {}))
            if ticket.seats_max > 0:
                ticket.seats_available = ticket.seats_max - (ticket.seats_reserved + ticket.seats_used)
                if ticket.event_id and ticket.event_id.seats_limited:
                        ticket.seats_available_event_limit = min(ticket.seats_available,ticket.event_id.seats_available)
