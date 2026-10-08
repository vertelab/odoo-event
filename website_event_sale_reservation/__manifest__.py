# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2022- Vertel Sverige AB (<https://vertel.se>).
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
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    'name': 'Event: Website Sale Reservation',
    'version': '18.0.1.0.0',
    # Version ledger: 18.0 = Odoo version. 1 = Major. Non regressionable code.
    # 0 = Minor. New features that are regressionable. 0 = Bug fixes
    'summary': 'Let website visitors reserve event seats before the event exists.',
    'category': 'Event',
    'description': """
        Website front-end for event reservations.

        Extends OCA/event_sale_reservation (the maintained 18.0 base) with:

        - A public booking form on the event page that lets a visitor reserve
          a seat even when the event is sold out or not yet scheduled. The
          reservation creates and confirms a sale order.
        - The ``event_reservation_ok`` product flag, which keeps reservation
          products separate from Odoo's ``service_tracking`` field.
        - A registration counter on the sale order with a direct link to the
          attendees.

        This module replaces the Vertel fork ``event_sale_reservation``
        (which depended on the unported ``web_ir_actions_act_view_reload``).
    """,
    'author': 'Vertel Sverige AB',
    'website': 'https://vertel.se/apps/odoo-event/website_event_sale_reservation',
    'images': ['static/description/banner.png'],  # 560x280 px.
    'license': 'AGPL-3',
    'maintainer': 'Vertel Sverige AB',
    'repository': 'https://github.com/vertelab/odoo-event',
    'maintainers': ['Vertelab'],
    'application': False,
    'installable': True,
    # OCA/event_sale_reservation is the maintained 18.0 base. It brings the
    # reservation model, the registration wizard and the sale.report column.
    'depends': [
        'event_sale_reservation',
        'website_event_sale',
    ],
    'data': [
        'views/product_template_view.xml',
        'views/event_templates_page_registration.xml',
    ],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
