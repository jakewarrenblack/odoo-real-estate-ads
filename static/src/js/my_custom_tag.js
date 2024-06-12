odoo.define('real_estate_ads.CustomAction', (require) => {
    // This is how you define a widget in Odoo

    'use strict';

    const AbstractAction = require('web.AbstractAction');
    const core = require('web.core');

    // Extend the AbstractAction class
    const CustomAction = AbstractAction.extend({
        template: "CustomActions",
        start: function() {
            console.log("Hello World!")
        }
    })

    // Register the widget
    // The first value is the name of the action as defined in the property_view.xml file
    core.action_registry.add("custom_client_action", CustomAction)

})