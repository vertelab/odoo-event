/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { rpc } from "@web/core/network/rpc";

// Catch registration form event, because of JS for attendee details
var EventWaitListRegistrationForm = publicWidget.Widget.extend({

    /**
     * @override
     */
    start: function () {
        var self = this;
        const post = this._getPost();
        const noTicketsOrdered = Object.values(post).map((value) => parseInt(value)).every(value => value === 0);
        var res = this._super.apply(this.arguments).then(function () {
            $('#waiting_list_form .a-submit')
                .off('click')
                .click(function (ev) {
                    self.on_click(ev);
                })
                .prop('disabled', noTicketsOrdered);
        });
        return res;
    },

    _getPost: function () {
        var post = {};
        $('#waiting_list_form select').each(function () {
            post[$(this).attr('name')] = $(this).val();
        });
        return post;
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {Event} ev
     */
    on_click: function (ev) {
        console.log('-------------------------')
        ev.preventDefault();
        ev.stopPropagation();
        var $form = $(ev.currentTarget).closest('form');
        var $button = $(ev.currentTarget).closest('[type="submit"]');
        const post = this._getPost();
        $button.attr('disabled', true);
        return rpc($form.attr('action'), post).then(function (modal) {
            var $modal = $(modal);
            $modal.find('.modal-body > div').removeClass('container'); // retrocompatibility - REMOVE ME in master / saas-19
            $modal.appendTo(document.body);
            const modalBS = new Modal($modal[0], {backdrop: 'static', keyboard: false});
            modalBS.show();
            $modal.appendTo('body').modal('show');
            $modal.on('click', '.js_goto_event', function () {
                $modal.modal('hide');
                $button.prop('disabled', false);
            });
            $modal.on('click', '.btn-close', function () {
                $button.prop('disabled', false);
            });
        });
    },
});

publicWidget.registry.EventWaitListRegistrationFormInstance = publicWidget.Widget.extend({
    selector: '#waiting_list_form',

    /**
     * @override
     */
    start: function () {
        var def = this._super.apply(this, arguments);
        this.instance = new EventWaitListRegistrationForm(this);
        return Promise.all([def, this.instance.attachTo(this.$el)]);
    },
    /**
     * @override
     */
    destroy: function () {
        this.instance.setElement(null);
        this._super.apply(this, arguments);
        this.instance.setElement(this.$el);
    },
});

export default EventWaitListRegistrationForm;
