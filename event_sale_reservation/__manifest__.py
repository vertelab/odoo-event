# Copyright 2021 Tecnativa - Jairo Llopis
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Sell event reservations",
    "summary": "Allow selling event registrations before the event exists",
    "version": "14.0.1.1.0",
    "development_status": "Beta",
    "category": "Marketing",
    "website": "https://github.com/OCA/event",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "maintainers": ["Yajo", "Vertelab"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
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
        "reports/event_registration_views.xml",
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
