# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Event Reservations",
    "summary": "Allow event registrations before the event exists",
    "version": "14.0.1.0.0",
    "category": "Event",
    "website": "https://vertlab.com",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "event_sale",
        "website_event",
        "web_ir_actions_act_multi",
        "web_ir_actions_act_view_reload",
        "product"
    ],
    "data": [
        "views/event_registration_views.xml",
        "views/event_templates_page_registration.xml",
        "views/assets.xml",
    ],
}
