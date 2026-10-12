# -*- coding: utf-8 -*-
{
    "name": "Skogsstyrelsen Utbildning Kundnöjdhetsrapport",
    "summary": "Creates a rating reports for events",
    "author": "Vertel Sverige AB",
    "contributor": "Marcus Jakobsson,Fredrik Arvas",
    "maintainer": "Vertel Sverige AB",
    "repository": "https://git.vertel.se/vertelab/odooext-skogsstyrelsen",
    "category": "Tools",
    "license": "AGPL-3",
    "version": "18.0.0.0.1",
    "website": "https://vertel.se",
    "description": """
        Creates a rating reports for events
    """,
    "depends": [
        "event",
        "rating",
    ],
    "data": [
        "views/event_rating_report.xml",
    ],
    "application": False,
    "installable": True,
}
