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

# Server Actions

These can do several things. Such as:

1. Execute Python code (most common)
2. Create record
3. Write record
4. Execute other server actions

Our example will extend the deadline of an offer. Imagine we wanted to move the deadline forward by increasing the validity duration.
If we had 1000 records, that would take forever.

A server action can select all records and update them in one go.