# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2024- Vertel Sverige AB (<https://vertel.se>).
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
    'name': 'Event: Elearning LMS',
    'version': '18.0.1.0.0',
    'summary': "Links events to e-learning courses.",
    'category': 'Event',
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-event/event_elearning',
    'images': ['/static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel Sverige AB',
    'repository': 'https://github.com/vertelab/odoo-event',
    'description': '''
Elearning LMS
=============

    Links events to e-learning courses.

    Features:

        - UI Integration: Extends 3 view(s) in the Odoo interface.
        - Extends Odoo: Builds on event.event, event.registration, event.type, slide.channel.
    ''',
    'depends': ['hr','event','website_slides', 'event_sale', 'event_waitlist_website'],
    'data': [
        'security/security.xml',
        'data/event_reminder_mail_templet.xml',
        'data/event_subscription_mail_templet.xml',
        'views/event_event.xml',
        #'views/menu.xml',
        'views/website_slides_templates_course.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
