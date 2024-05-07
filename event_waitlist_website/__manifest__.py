# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2022- Vertel AB (<https://vertel.se>).
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
# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Event Waitlist Website',
    'version': '17.0.1.0.0',
    'summary': 'Allow event waitlist on event template from website.',
    'category': 'Event',
    'description': """
        Allow event waitlist on event template from website.
    """,
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-event/event_waitlist_website',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-event',
    "application": True,
    "installable": True,
    # 'depends': ['event_sale','website_event','web_ir_actions_act_multi','web_ir_actions_act_view_reload','product',],
    'depends': ['event_sale','website_event','product',],
    "data": [
        'security/ir.model.access.csv',
        'views/event_type_templates.xml',
        'views/event_type_view.xml',
        'views/event_waiting_list_view.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'event_waitlist_website/static/src/js/website_event.js',
        ],
    },
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
