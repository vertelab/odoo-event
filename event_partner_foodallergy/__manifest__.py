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
    'name': 'Event Partner Food Allergy',
    'summary': 'Extends the event registration form view with an option about foodallergy.',
    'author': 'Vertel AB',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-event',
    'version': '14.0.0.1',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'license': 'AGPL-3',
    'website': 'https://vertel.se/apps/event-partner',
    'description': """
        Extends the event registration form view with an option about foodallergy\n\n
        Features:\n
            *   Adds a "Food Is Served" check box on events. If its checked, the field "Food allergy" will be added to the\n
                attendees of the event.\n
            *   Adds a question about food allergy to the event registration form. The question is only visible if "Food Is Served"\n
                is checked for the event.\n
        This module is maintained from: https://github.com/vertelab/odoo-event/tree/14.0/event_partner_foodallergy/\n
    """,
    'depends': ['event','website_event'],
    'data': [
        'views/foodallergy_view.xml',
        'views/templates.xml',
    ],
    'installable': True,
}
