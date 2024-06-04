from odoo import fields, models


# Import model from the models class
class Property(models.Model):
    _name = "estate.property"  # this is a table in the database, and the attributes below are its columns/attributes

    name = fields.Char(string="Name")

    # Here's how we make a relationship between the two models
    type_id = fields.Many2one("estate.property.type", string="Property Type")

    # The convention of many to many is to pluralise the attribute name
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")

    description = fields.Text(string="Description")  # multiline values
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Date")
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price")
    best_offer = fields.Float(string="Best Offer")
    bedrooms = fields.Integer(string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garden = fields.Boolean(string="Garden", default=False)
    garage = fields.Boolean(string="Garage", default=False)
    garden_area = fields.Integer(string="Garden Area")
    garden_orientation = fields.Selection(
        [('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        string="Garden Orientation",
        default='north'
    )

    # Here we tie the offer to the property
    # One2Many relationships are different from the others,
    # in that they must have an inverse_name attribute provided, as well as the comodel name
    # So this is the inverse of the link we made using Many2One in property_offer
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Offers")

    # A salesperson. res.users is another model available to use once we have the base
    sales_id = fields.Many2one('res.users', string='Salesman')
    # https://stackoverflow.com/questions/22927605/what-is-res-partner
    # Again, the partner represents people and organisations
    buyer_id = fields.Many2one('res.partner', string='Buyer')


# We'll have a many-to-one relationship between a property and its type (e.g. apartment or house)
# So again we just define a class for our model and its attributes
# It will have its own view too
class PropertyType(models.Model):
    _name = "estate.property.type"

    name = fields.Char(string="Name", required=True)


# There will be a many-to-many relationship between a property and its descriptive tags
class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Name", required=True)
