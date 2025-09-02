# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2024- Vertel AB (<https://vertel.se>).
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
#
# https://www.odoo.com/documentation/14.0/reference/module.html
#
{
    'name': 'Event: Website Event Portal Elearning Glue',
    'version': '0.1',
    'summary': '',
    'category': 'Event', # Technical Settings|Localization|Payroll Localization|Account Charts|User types|Invoicing|Sales|Human Resources|Operations|Marketing|Manufacturing|Website|Theme|Administration|Appraisals|Sign|Helpdesk|Administration|Extra Rights|Other Extra Rights|
    'description': """
    
    """,
    #'sequence': 1,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-event/website_event_portal_elearning',
    'images': ['static/description/banner.png'], # 560x280
    'license': 'AGPL-3',
    'depends': ['website_event_portal', 'event_lms'],
     #"external_dependencies": {
     #   "bin": ["openssl",], 
     #   "python": ["acme_tiny", "IPy",],
     #},
    'data': ['views/event_portal_templates.xml'],
    'demo': [],
    'application': False,
    'installable': True,    
    'auto_install': False,
    #"post_init_hook": "post_init_hook",
}
