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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'HR Partner Event',
    'summary': 'To be able to have multiple partners on event.',
    'author': 'Vertel AB',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://git.vertel.se/vertelab/odoo-event'
    'category': 'Employee',
    'version': '14.0.0.2',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'website': 'https://vertel.se',
    'description': """
        To be able to have multiple partners on event. \n
        14.0.0.1
            - Changed Maximum seat to Available seat
            - Improved access right for event partners
        14.0.0.2
            - Improvement to Event Access Right
            - Added the available seats to tree and form view
    """,
    'author': 'Vertel AB',
    'website': 'https://www.vertel.se',
    'depends': ['website_event', 'event'],
    'data': [
        'views/event_event_view.xml',
        'views/event_template.xml',
    ],
    'application': True,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4s:softtabstop=4:shiftwidth=4:
