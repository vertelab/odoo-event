# -*- coding: utf-8 -*-
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
    'name': 'Event Type Webpage',
    'summary': 'Allows for more control of the appearance of an using event templates',
    'author': 'Vertel AB',
    'maintainer': 'Vertel AB',
    'repository': 'https://git.vertel.se/vertelab/odoo-event',
    'category': 'Employee',
    'version': '14.0.0.1.0',
    'license': 'AGPL-3',
    'description': """
        14.0.0.1.0
           -added Go to Website on Event Type.   
    """,
    'depends': ['website_event', 'event', 'event_webpage'],
    'data': [
        'views/event_type_view.xml',
        'views/event_type_template.xml',
    ],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
