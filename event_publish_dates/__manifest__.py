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
    'name': 'Event Publish Dates',
    'version': '14.0.0.2',
    'category': 'Event',
    'summary': 'Extends the website event publish date',
    'description': """
        Extends the website event publish date\n\n
        Features:\n
            *   Two fields were added for a publishing date and un-publishing date. \n
            *   Added cron job to auto publish event on website and also un-publish. \n
    """,
    'author': 'Vertel AB',
    'website': 'https://www.vertel.se',
    'depends': ['event', 'website_event'],
    'data': [
        'views/event_view.xml',
        'data/data.xml',
    ],
    'installable': True,
}
