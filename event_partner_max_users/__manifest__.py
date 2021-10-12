# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution, third party addon
#    Copyright (C) 2021- Vertel AB (<http://vertel.se>).
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
    'name': 'Event Partner Max Users',
    'version': '14.0.0.1',
    'category': 'Event',
    'summary': 'Extends the event registration form view with visible information about the size of the event',
    'description': """
        Extends the event registration form view with visible information about the size of the event\n\n
        Features:\n
            *   Adds visible information about the size of the event.\n
        This module is maintained from: https://github.com/vertelab/odoo-event/tree/14.0/event_partner_max_users/\n
    """,
    'author': 'Vertel AB',
    'website': 'https://www.vertel.se',
    'depends': ['event','website_event'],
    'data': [
        'views/templates.xml',
    ],
    'installable': True,
}
