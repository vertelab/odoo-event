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
    'name': 'Event: Sale Reservation',
    'version': '14.0.1.1.0',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'Allow selling event registrations before the event exists.',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Event',
    'description': """
    To sell event reservations.
    """,
    #'sequence': '1',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-event/event_sale_reservation',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer':  ['Yajo', 'Vertel AB'],
    'repository': 'https://github.com/vertelab/odoo-event',
    # Any module necessary for this one to work correctly
    "depends": [
        "event_sale",
        "website_event",
        "web_ir_actions_act_multi",
        "web_ir_actions_act_view_reload",
        "product",
        "partner_gender"
    ],
    "data": [
        "reports/sale_report_view.xml",
        "wizards/registration_editor_view.xml",
        "views/event_type_view.xml",
        "views/product_template_view.xml",
        "views/sale_order_view.xml",
        "views/event_templates_page_registration.xml",
        "views/assets.xml",
    ],
    # These modules makes totals wrong because they depend currently on count
    # and not sum of qtys; integrating with them would require a glue module
    "excludes": ["event_registration_multi_qty", "event_sale_registration_multi_qty"],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
