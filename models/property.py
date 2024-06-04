from odoo import fields, models


# Import model from the models class
class Property(models.Model):
    _name = "estate.property"  # this is a table in the database, and the attributes below are its columns/attributes

    name = fields.Char(string="Name")

    # Here's how we make a relationship between the two models
    type_id = fields.Many2one("estate.property.type", string="Property Type")

    description = fields.Text(string="Description")  # multiline values
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date")
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price")
    best_offer = fields.Float(string="Best Offer")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation",
        default='north'
    )

# We'll have a many-to-one relationship between a property and its type (e.g. apartment or house)
# So again we just define a class for our model and its attributes
# It will have its own view too
class PropertyType(models.Model):
    _name = "estate.property.type"

    name = fields.Char(string="Name", required=True)