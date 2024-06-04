from odoo import fields, models


# Import model from the models class
class Property(models.Model):
    _name = "estate.property"  # this is a table in the database, and the attributes below are its columns/attributes

    name = fields.Char(string="Name")
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
