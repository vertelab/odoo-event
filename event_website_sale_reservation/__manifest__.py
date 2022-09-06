# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Website Event Sale Reservations",
    "summary": "Add VAT information to event sale page",
    "version": "14.0.1.0.0",
    "development_status": "Beta",
    "category": "Marketing",
    "website": "https://github.com/vertelab/odoo-event",
    "author": "Vertel AB",
    "maintainers": ["Vertelab"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "website_event_sale",
    ],
    "data": [
        "views/event_website_sale_reservation.xml",
    ],
}
