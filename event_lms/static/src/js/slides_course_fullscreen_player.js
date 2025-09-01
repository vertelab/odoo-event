/** @odoo-module **/

import publicWidget from '@web/legacy/js/public/public_widget';
import Fullscreen from '@website_slides/js/slides_course_fullscreen_player';

/**
 * Helper: Get the slide dict matching the given criteria
 *
 * @private
 * @param {Array<Object>} slideList List of dict representing a slide
 * @param {[string] : any} matcher
 */
var findSlide = function (slideList, matcher) {
    return slideList.find((slide) => {
        return Object.keys(matcher).every((key) => matcher[key] === slide[key]);
    });
};

// Extend the Fullscreen widget to handle event_type slides
var EventTypeFullscreen = Fullscreen.include({

    init: function (parent, slides, defaultSlideId, channelData) {
        var result = this._super(parent, slides, defaultSlideId, channelData);
        console.log("EventTypeFullscreen initialized");
        return result;
    },

    /**
     * Override the sidebar's _onClickTab method to handle event_type slides
     */
    start: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function() {
            // Override the sidebar's click handler
            if (self.sidebar) {
                self.sidebar._onClickTab = self._onSidebarClickTab.bind(self);
            }
        });
    },

    /**
     * Custom click handler for sidebar that handles event_type slides
     */
    _onSidebarClickTab: function (ev) {
        ev.stopPropagation();
        const $elem = $(ev.currentTarget).closest('.o_wslides_fs_sidebar_list_item');

        console.log("Custom click handler triggered");
        console.log("Element data:", $elem.data());

        if ($elem.data('canAccess') === 'True') {
            const slideCategory = $elem.data('category');
            console.log("Slide category:", slideCategory);

            // Check if this is an event_type slide
            if (slideCategory === 'event_type') {
                // Get the event_type_id from the slide data
                const eventTypeId = $elem.data('eventTypeId');
                console.log("Event type ID:", eventTypeId);

                if (eventTypeId) {
                    // Redirect to the event-type URL instead of handling internally
                    console.log("Redirecting to:", `/event-type/${eventTypeId}`);
                    window.location.href = `/event-type/${eventTypeId}`;
                    return;
                }
            }

            // Default behavior for non-event_type slides
            var isQuiz = $elem.data('isQuiz');
            var slideID = parseInt($elem.data('id'));
            var slide = findSlide(this.slides, {id: slideID, isQuiz: isQuiz});
            this.sidebar._updateSlideEntry(slide);
        }
    }, // <- Added missing comma here

    /**
     * Override _onChangeSlideRequest to handle event_type slides
     */
    _onChangeSlideRequest: function (ev) {
        var slideData = ev.data;
        var newSlide = findSlide(this.slides, {
            id: slideData.id,
            isQuiz: slideData.isQuiz || false,
        });

        // Check if this is an event_type slide by looking at the DOM
        var $slideElem = this.$('.o_wslides_fs_sidebar_list_item[data-id="' + slideData.id + '"]');
        var slideCategory = $slideElem.data('category');

        if (slideCategory === 'event_type') {
            var eventTypeId = $slideElem.data('eventTypeId');
            if (eventTypeId) {
                console.log("Redirecting to event_type:", `/event-type/${eventTypeId}`);
                window.location.href = `/event-type/${eventTypeId}`;
                return;
            }
        }

        // Default behavior for non-event_type slides
        this._super.apply(this, arguments);
    }
});

export default EventTypeFullscreen;