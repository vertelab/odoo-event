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
    'name': 'Event: Tier Validation',
    'version': '14.0.0.0.0',
    'summary': """
        Extends the functionality of Event Type to
        support a tier validation process
    """,
    'category': 'Event',
    'description': """
        Long description of module's purpose
    """,
    #'sequence': 1,
    'images': ['static/description/banner.png'], # 560x280 px.
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-event/event_tier_validation',
    'license': 'AGPL-3',
     #"external_dependencies": {
     #   "bin": ["openssl",], 
     #   "python": ["acme_tiny", "IPy",],
     #},
    "data": ["views/event_event_view.xml"],
    "depends": ["event", "base_tier_validation"],
    'application': False,
    'installable': True,    
    'auto_install': False,
    #"post_init_hook": "post_init_hook",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
