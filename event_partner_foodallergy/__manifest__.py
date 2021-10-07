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
    'name': 'Event Partner Food Allergy',
    'version': '14.0.0.1',
    'category': 'Event',
    'summary': 'Extends the event registration form view with an option about foodallergy',
    'description': """
        Extends the event registration form view with an option about foodallergy
    """,
    'author': 'Vertel AB',
    'website': 'https://www.vertel.se',
    'depends': ['event','website_event'],
    'data': [
        'views/foodallergy_view.xml',
        'views/templates.xml',
    ],
    'application': True,
    'installable': True,
}
