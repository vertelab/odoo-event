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
    'name': 'Event Filtered Dropdown',
    'summary': 'Filter organizer and venue dropdown',
    'author': 'Vertel AB',
    'category': 'Event',
    'version': '14.0.0.2',
    'license': 'AGPL-3',
    'website': 'https://vertel.se',
    'description': """
        14.0.0.2
            - Defaulted website checkout country to Sweden and flipped zip and city
            -  Defaulted timezone to Europe/Stockholm and added field to debug group
    """,
    'depends': ['website_event', 'event', 'base'],
    'data': [
        'views/event_view.xml',
        'views/templates.xml',
    ],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
