# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo SA, Open Source Management Solution, third party addon
#    Copyright (C) 2024- Vertel AB (<https://vertel.se>).
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
    'name': 'Event: Learning Experience Platform',
    'version': '1.0',
    # Version ledger: 14.0 = Odoo version. 1 = Major. Non regressionable code. 2 = Minor. New features that are regressionable. 3 = Bug fixes
    'summary': 'Adds AI-driven functionality to the LX-plattform in Event/e-learning.',
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Event',
    'description': """
Adds AI-driven functionality to the LX-plattform in Event/e-learning.
Odoo Learning Experience Platform (LXP) is an innovative and AI-powered extension of Odoo e-learning, designed to provide a personalized and engaging educational experience. The module is a complement to gamification and other collaboration functions.
This platform integrates advanced AI technology to offer personalized recommendations and content tailored to the user's interests and skills.

At the heart of Odoo LXP is user-driven interactivity. Students have complete freedom to create and share their own content, which promotes a dynamic and inclusive learning environment. Using the platform's intuitive tools, users can easily create lessons, upload images, and start polls to engage their fellow students. This makes learning a collective experience where everyone can contribute and grow together.

The AI ​​technology in Odoo LXP continuously analyzes users' behavior and learning style to offer personalized recommendations. These recommendations include courses, articles, videos and other educational resources relevant to the user's individual needs and goals. The system takes into account past activities, interests and achievements to ensure that each user receives an optimized learning journey.

An important feature of Odoo LXP is the ability to like and share other people's content. This fosters a culture of sharing and collaboration where students can inspire and learn from each other. The platform also encourages cross-functional collaboration through specialized collaboration groups (channels). These groups enable users from different departments or areas of interest to work together, share insights and solve problems together.

Odoo LXP creates a coherent learning environment that breaks down traditional barriers in education. By combining personalized AI technology with a strong user-driven component, the platform offers an engaging and personalized experience that promotes continuous development and collaboration. This platform represents the future of learning, where every student has the opportunity to shape their own educational path and benefit from the collective intelligence of the community. 
    """,
    #'sequence': '1',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-event/event_lxp',
    'images': ['static/description/banner.png'], # 560x280 px.
    'license': 'AGPL-3',
    'contributor': '',
    'maintainer': 'Vertel AB',
    'repository': 'https://github.com/vertelab/odoo-event',
    # Any module necessary for this one to work correctly
    'depends': ['website_event', 'event', 'base', 'portal'],
    'data': [
        #'security/ir.model.access.csv',
        #'views/event_views.xml',
    ],
    'application': False,
    'installable': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
