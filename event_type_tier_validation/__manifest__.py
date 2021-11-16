# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) {year} {company} (<{mail}>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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
#
# https://www.odoo.com/documentation/14.0/reference/module.html
#
{
    'name': 'Event Type Tier Validation',
    'version': '14.0.0.0.0',
    'summary': """
        Extends the functionality of Event Type to
        support a tier validation process
    """,
    'category': 'Event', # Technical Settings|Localization|Payroll Localization|Account Charts|User types|Invoicing|Sales|Human Resources|Operations|Marketing|Manufacturing|Website|Theme|Administration|Appraisals|Sign|Helpdesk|Administration|Extra Rights|Other Extra Rights|
    'description': """
        Long description of module's purpose
    """,
    #'sequence': 1,
    'images': ['static/descrition/banner.svg'],
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/',
    'license': 'AGPL-3',
     #"external_dependencies": {
     #   "bin": ["openssl",], 
     #   "python": ["acme_tiny", "IPy",],
     #},
    "data": ["views/event_type_view.xml"],
    "depends": ["event", "base_tier_validation"],
    'application': False,
    'installable': True,    
    'auto_install': False,
    #"post_init_hook": "post_init_hook",
}