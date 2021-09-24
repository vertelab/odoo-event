##############################################################################
#
#    OpenERP, Open Source Management Solution, third party addon
#    Copyright (C) 2004-2021 Vertel AB (<http://vertel.se>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Event Partner Calendar',
    'version': '14.0.0.0.1',
    'category': '',
    'summary': 'New events are shown in the calendar',
    'description': """
        Newly created events creates corresponding entries in the calendar.\n\n
        Features:\n
            * The start/end-time of the calendar entry is updated when the start/end time of the event changes.\n
            * Attendees of the event are added to the calendar event when they are added/removed to/from the event.\n
            * The calendar entry is removed when the event is removed.\n\n
        This module is maintained from: https://github.com/vertelab/odoo-event/tree/14.0/event_partner_calendar/ \n
""",
    'author': "Vertel AB",
    'license': "AGPL-3",
    'website': 'https://www.vertel.se',
    'depends': ['event','calendar'],
    'data': [],
    'installable': True,
}
