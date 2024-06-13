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

# Report Actions

These are used to generate reports. They can be triggered from the client or server side.

They can be used to generate PDFs, Excel files, etc.

To create a custom report action:

1. In the `report` directory, create a file to contain the record for the report action.

E.g.

```xml
<odoo>
    <data>
        <record id="property_report_action" model="ir.actions.report" >
            <field name="name">Property Report Action</field>
            <field name="model">estate.property</field>
            <field name="report_type">qweb-pdf</field>
            <!-- Format: <module_name>.report_<model_name> -->
            <field name="report_name">real_estate_ads.report_estate_property</field>
            <field name="report_file">real_estate_ads.report_estate_property</field>
            <!-- So the report will always use the name of our current property -->
            <!-- _get_report_base_filename() is a method we will define in the property model -->
            <field name="print_report_name">(object._get_report_base_filename())</field>
            <field name="binding_model_id" ref="real_estate_ads_model_estate_property"/>
            <field name="binding_type">report</field>
            <!-- Restrict which groups can access this report -->
            <field name="groups_id" eval="[(4, ref('real_estate_ads.group_property_manager'))]"/>
            <!-- To determine the filename of the report -->
            <field name="attachment">((object.name)+'.pdf')</field>
        </record>
    </data>
</odoo>
```

2. You might need to define some functions, such as we have above. These can be defined in the model.

In this specific case, we'll need this one:

```py
def _get_report_base_filename(self):
    # ensure_one() makes sure we only have one record at the point of query
    self.ensure_one()
    return f'Estate Property - {self.name}'
```

3. Create your qweb template, also in the `report` directory.

E.g.

```xml
<odoo>
    <data>
        <template id="report_estate_property_document">
            <t t-call="web.external_layout">
                <div class="mt-5">
                    <div class="page">
                        <h2>Property Report</h2>
                    </div>
                </div>
            </t>    
        </template>
        
        <template id="report_estate_property">
            <t t-call="web.html_container">
                <t t-foreach="docs" t-as="o">
                    <t t-call="real_estate_ads.report_estate_property_document"/>
                </t>
            </t>
        </template>
    </data>
</odoo>
```

#### t-call

`t-call` is a qweb syntax used to reference another template.

So above we pull in the `html_container` template from the web module.

We also pull in our custom template `report_estate_property_document`, which we've just defined in the same file.

#### docs

`docs` is a special variable in qweb. It's a list of records that are passed to the template.

The `t-as` attribute is used to assign a name to each record in the list. Just like a normal loop.

4. Import all this stuff into the manifest.

It seems in the case of a report action, you don't need to define a menu item.
Simply by saying that the report action exists, it will show up under the `Print` menu.
