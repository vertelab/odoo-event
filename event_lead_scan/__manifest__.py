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

{
    'name': 'Event: Lead Scanning',
    'version': '18.0.1.0.0',
    # Version ledger: 18.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'Scan attendee badges at events and capture CRM leads.',
    'category': 'Event',
    'description': '''
Event Lead Scanning
===================

Exhibitors scan attendee badge QR codes at an event and capture CRM
leads, linked to the event and the registration.

Features:
    - Scan session per exhibitor or staff member
    - QR code on the attendee badge (scan token per registration)
    - Mobile web scanner, no native app and no Odoo account required
    - Offline queue: scans are kept locally and synced when online
    - Leads land in CRM with note and score, ready for follow-up
''',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-event/event_lead_scan',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-event',
    'depends': ['event', 'website_event', 'crm', 'event_partner'],
    'data': [
        'security/event_lead_scan_security.xml',
        'security/ir.model.access.csv',
        'views/event_lead_scan_session_views.xml',
        'views/crm_lead_views.xml',
        'views/event_event_views.xml',
        'views/event_registration_views.xml',
        'views/scan_templates.xml',
        'report/event_attendee_badge_scan.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'event_lead_scan/static/src/js/scan_queue.js',
            'event_lead_scan/static/src/js/scan_app.js',
        ],
    },
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
