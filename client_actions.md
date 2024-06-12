# Client Actions

Triggers the actions implemented on the client.

They are menu items defined in the XML. The corresponding action is tied to a widget, which is written in JavaScript.

It's simple to create a client action triggered based on existing widgets.

To have a custom one with a tag which does not exist in odoo:

1. Create a menu item
1. Create an action
2. Link the action to the menu item
3. Create a widget (JavaScript)
4. Create a view (XML)