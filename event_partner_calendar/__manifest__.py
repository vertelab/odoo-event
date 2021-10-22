##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2021- Vertel AB (<https://vertel.se>).
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
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'Event Partner Calendar',
    'summary': 'New events are shown in the calendar',
    'author': "Vertel AB",
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'git@github.com:vertelab/odoo-event.git'
    'category': 'Tools',
    'license': 'AGPL-3',
    'version': '14.0.0.0.1',
    'website': 'https://vertel.se',
    'description': """
        Newly created events creates corresponding entries in the calendar.\n\n
        Features:\n
            * The start/end-time of the calendar entry is updated when the start/end time of the event changes.\n
            * Attendees of the event are added to the calendar event when they are added/removed to/from the event.\n
            * The calendar entry is removed when the event is removed.\n\n
        This module is maintained from: https://github.com/vertelab/odoo-event/tree/14.0/event_partner_calendar/ \n
""",
    'depends': ['event','calendar'],
    'data': [],
    'installable': True,
}
