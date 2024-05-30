from odoo import fields, models

# Creating a model
class Property(models.Model):
    # representing a table in our database
    _name = 'estate.property'

    # representing columns in our table
    # The values here will be what show up in the view
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description") # Text is multiline
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price")
    best_offer = fields.Float(string="Best Offer")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage", default=False)
    garden = fields.Boolean(string="Garden", default=False)
    garden_area = fields.Integer(string="Garden Area")
    # List of tuples
    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        string="Garden Orientation",
        default='north'
    )

    # id, create_date, create_uid, write_date, write_uid - odoo also creates these fields automatically
