from odoo import fields, models, api


class Property(models.Model):
    _name = 'estate.property'
    _description = 'Estate Properties'

    name = fields.Char(string="Name", required=True)
    state = fields.Selection([
        ('new', 'New'),
        ('received', 'Offer Received'),
        ('accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancel', 'Cancelled')
    ], default='new', string="Status", group_expand='_expand_state')

    # Here's how we make a relationship between the two models
    type_id = fields.Many2one("estate.property.type", string="Property Type")

    # The convention of many to many is to pluralise the attribute name
    tag_ids = fields.Many2many('estate.property.tag', string="Property Tag")

    description = fields.Text(string="Description")  # multiline values
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(string="Available From")
    expected_price = fields.Float(string="Expected Price")
    selling_price = fields.Float(string="Selling Price", readonly=True)
    best_offer = fields.Float(string="Best Offer", compute='compute_best_price')
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

    buyer_id = fields.Many2one(
        # https://stackoverflow.com/questions/22927605/what-is-res-partner
        # Again, the partner represents people and organisations
        'res.partner',
        string='Buyer',
        # Domain filtering:
        # For the sake of an example, we can filter out specific types of partners.
        # Since they could be companies or individuals, we can filter for one or the other
        # So 'is_company' is just one of the attributes available on res.partner
        # For other types like integers, we could check less than, greater than, etc.
        domain=[('is_company', '=', True)]
    )

    # We said that we have a many2one relationship between property and partner in the form of buyer_id
    # Partners have phone numbers,
    # so we can access that by saying that 'phone' is equal to a
    # 'related' value of buyer_id (which is on this model) .phone, taken from the partner
    phone = fields.Char(string="Phone", related='buyer_id.phone')

    @api.onchange('living_area', 'garden_area')
    def _onchange_total_area(self):
        self.total_area = self.living_area + self.garden_area

    total_area = fields.Integer(string="Total Area")

    def action_sold(self):
        self.state = 'sold'

    def action_cancel(self):
        self.state = 'cancel'

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = len(rec.offer_ids)

    offer_count = fields.Integer(string="Offer Count", compute=_compute_offer_count)

    def action_property_view_offers(self):
        return {
            'type': 'ir.actions.act_window',
            'name': f"{self.name} - Offers",
            'domain': [('property_id', '=', self.id)],
            'view_mode': 'tree',
            'res_model': 'estate.property.offer',

        }

    @api.depends('offer_ids')
    def compute_best_price(self):
        for rec in self:
            if rec.offer_ids:
                rec.best_offer = max(rec.offer_ids.mapped('price'))
            else:
                rec.best_offer = 0

    '''
    When you use the context="{'group_by': 'field_name'}" attribute in a filter within a search view, 
    Odoo will look for a method named _expand_field_name in the corresponding model. 
    This method should return a list of tuples, 
    where each tuple represents a possible state and contains two elements: 
    the internal value of the state and the display name of the state
    '''

    @api.model
    def _expand_state(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    # def action_client_action(self):
    #     return {
    #         'type': 'ir.actions.client',
    #         #'tag': 'reload'  # A widget for this tag already exists out of the box, it will refresh the page
    #         # Others:
    #         # 'apps' - open the app page
    #         # 'display_notification' - display a notification.
    #         # You'll use the 'params' tag alongside this, as well as a notification type, e.g.
    #         # 'tag': 'display_notification',
    #         # 'params': {'title': 'Title', 'message': 'Message', 'type': 'success', 'sticky': False},
    #     }

    def action_url_action(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.odoo.com',
            'target': 'new' # or can be 'self' to open in the same tab
        }

    def _get_report_base_filename(self):
        # ensure_one() makes sure we only have one record at the point of query
        self.ensure_one()
        return f'Estate Property - {self.name}'


class PropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Property Type'

    name = fields.Char(string="Name", required=True)


class PropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Property Tag'

    name = fields.Char(string="Name", required=True)
    color = fields.Integer(string="Color")
