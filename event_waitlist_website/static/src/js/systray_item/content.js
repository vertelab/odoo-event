/** @odoo-module **/

import { NewContentModal, MODULE_STATUS } from '@website/systray_items/new_content'
import { patch } from '@web/core/utils/patch'
import { _t } from "@web/core/l10n/translation";
import { Component, xml } from "@odoo/owl";

patch(NewContentModal.prototype, {
    setup() {
        super.setup();

        const elementIndex = this.state.newContentElements.findIndex(
            element => element.moduleXmlId === 'website_event_type'
        );

        if (elementIndex === -1) {
            const newElement = {
                moduleName: 'website_event',
                moduleXmlId: 'website_event_type',
                status: MODULE_STATUS.NOT_INSTALLED,
                icon: xml`<i class="fa fa-calendar-o"/>`,
                title: _t('Event Type'),
            };
            this.state.newContentElements.push(newElement)
        } else {
            console.log('New content element already exists:', this.state.newContentElements[elementIndex]);
        }

        const newEventType = this.state.newContentElements.find(
            element => element.moduleXmlId === 'website_event_type'
        );

        newEventType.createNewContent = () => this.onAddContent('event_waitlist_website.event_type_action_add', true);
        newEventType.status = MODULE_STATUS.INSTALLED;
        newEventType.model = 'event.type';
    }
})