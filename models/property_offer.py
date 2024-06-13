from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offers'

    # Give offers semi-unique names
    @api.depends('property_id', 'partner_id')
    def _compute_name(self):
        for rec in self:
            if rec.property_id and rec.partner_id:
                rec.name = f'{rec.partner_id.name} - {rec.property_id.name}'
            else:
                rec.name = False

    name = fields.Char(string='Description', compute='_compute_name')

    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')], string='Status')
    # The entity placing the bid/offer will be a customer, but there's an entity in Odoo called res.partner
    # Partners represent people or organisations,
    # so we can use res.partner as our 'customer' instead of making a model for that
    partner_id = fields.Many2one('res.partner', string='Customer')

    # estate.property must be linked to this offer model via the property ID
    property_id = fields.Many2one('estate.property', string='Property')

    # We can compute the deadline of an offer based on when it was made x the validity duration
    validity = fields.Integer(string="Validity")  # E.g., '5' as in 'valid for 5 days'
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline')

    @api.model
    def _set_creation_date(self):
        return fields.Date.today()

    creation_date = fields.Date(string="Creation Date", default=_set_creation_date)

    @api.depends('validity', 'creation_date')
    def _compute_deadline(self):
        for rec in self:
            if rec.creation_date and rec.validity:
                # Pass in the validity duration to calculate delta of 5 days
                rec.deadline = rec.creation_date + timedelta(days=rec.validity)
            else:
                rec.deadline = False

    # Keep in mind that inverse does its work when the record is saved, while compute does it on the fly
    def _inverse_deadline(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                # They're date objects, so have access to 'days' attribute
                rec.validity = (rec.deadline - rec.creation_date).days
            else:
                rec.validity = False

    '''
    This decorator is like a garbage collector
    Oddo runs a daily cron job called auto-vacuum
    This decorator means we avoid writing a custom cron job to clean something up
    And instead just add our function to the tasks carried out by the autovacuum
    Such as:
    
    @api.autovacuum
    def _clean_offers(self):
        self.search([('status', '=', 'refused')]).unlink() # unlink() deletes records
    '''

    # This is used for applying a method to the model as a whole
    # It doesn't operate on a specific record. The model is relevant, its contents are not.
    # A common use-case would be creating a new record
    # So, you're just adding your CRUD functionality for example. Or even:
    '''
    @api.model
    def _set_create_date(self):
        # This makes sense, the contents of the record are irrelevant, only the model itself.
        return fields.Date.today()
    '''

    # This one allows creating multiple records from a dict or list of dicts
    # It also allows updating values before creation
    # Or, you can add some other stuff after creation using this decorator
    # It's mostly used with the create() ORM method

    # By creating multiple records in a single call, you minimise the overhead of multiple database transactions
    # So it makes sense to use this when we have some operation to perform on lots of records, e.g. when creating

    '''
    @api.model_create_multi
    def create(self, vals):
        # The parameter vals_list is a list of dictionaries, where each dictionary represents a record to be created.
        
        # It's a good idea to loop and check if exists
        for rec in vals:
            if not rec.get('creation_date'):
                rec['creation_date'] = fields.Date.today()
                 
        # Use super() to call the original create method with the updated list of dictionaries
        return super(PropertyOffer, self).create(vals)
         
    '''

    '''
    Once you customise the create method with the @api.model_create_multi decorator in a model, 
    you don't need to explicitly call this method anywhere in your code. 
    The customised create method will be automatically used whenever you create records for that model using Odoo's ORM.
    '''

    '''
    We saw this one earlier, using it to calculate a computed field value:
    
    @api.depends(*args): 
    Decorator used to specify dependencies for computed fields. When the fields listed in the 
    arguments change, the decorated method is automatically called to recompute the value of the dependent field.
    '''

    # Preventing an operation from happening when constraints are not met:
    '''
    @api.constrains()
    '''

    # Example:
    @api.constrains('validity')
    def _check_validity(self):
        for rec in self:
            if rec.deadline and rec.creation_date:
                if rec.deadline <= rec.creation_date:
                    raise ValidationError("Deadline cannot be before creation date")

    #########################################################################################
    # ORM methods: Odoo provides CRUD functionality we can override
    #########################################################################################

    # Create
    # @api.model_create_multi
    # def create(self, vals):
    #     # Example here is overriding the default create method, so we can modify the creation_date attribute as needed
    #     for rec in vals:
    #         if not rec.get('creation_date'):
    #             rec['creation_date'] = fields.Date.today()
    #
    #     # Always remember to return the super method of the ORM method you are overriding at the end
    #     return super(PropertyOffer, self).create(vals)

    # Write: Update all records in self with the provided value.
    # It's triggered when there's any change in the record.
    # def write(self, vals):
    #     # So, when some change is made to a property offer (and the offer is saved), we'd see the value printed out
    #     print(vals)
    #
    #     # Updated values are returned into the super() call to update the record
    #     return super(PropertyOffer, self).write(vals)

    # Miracle talks about search and browse. I was confused as to the difference between these.
    # https://stackoverflow.com/questions/29279442/need-explanation-of-syntax-and-use-of-search-browse-return-variables
    # Search accepts some filter (domain)  as an argument and returns a list of IDs.
    # Browse seems to accept an ID as an argument and returns browsable records.
    # In his example, within the write method above, we could find something like:

    '''
    print(vals) # Just to see what the values are
    
    res_partner_ids = self.env['res.partner'].search([
        ('is_company', '=', True)
    ])
    
    print(res_partner_ids.name) 
    '''

    # Which would return:
    # 1. The values provided when the write operation occurs
    # 2. The record where that search filter is true
    '''
        => {'price': 40}
        => 'Joe Bloggs'
    '''

    # Search also accepts a 'limit' parameter
    # As well as an order parameter. Such as order='name asc'

    '''
    Another one to keep in mind is search_count() -> Rather than returning the actual record, it tells the number of records which match your given condition.
    '''

    '''
    Also keep in mind that you can run the .unlink() method on any of these queries, to delete the records which are found.
    '''

    '''
    You can also override the unlink method.
    
    An obvious use case be implementing some cascading delete, whereby you delete some partner who has associated records of some kind.
    '''

    '''
    
    More methods you can chain onto your domain search:
    .mapped() -> Return some specific attribute
    
    .filtered() -> Filter out records on the fly without needing to append to some list and filter manually:
        e.g., .filtered(lambda x: x.phone == '085 111 1111')
        
    '''

    def action_accept_offer(self):
        if self.property_id:
            # You can do it this way
            # self.property_id.selling_price = self.price

            self._validate_accepted_offer()

            # Or use the ORM method
            self.property_id.write({
                'selling_price': self.price,
                'state': 'accepted'
            })

            self.status = 'accepted'

    # Ensure only one offer can be accepted
    def _validate_accepted_offer(self):
        # Find the property related to this offer by ID
        # Then search for any *other* offers related to that property which have been accepted
        offer_ids = self.env['estate.property.offer'].search([
            ('property_id', '=', self.property_id.id),
            ('status', '=', 'accepted')
        ])

        if offer_ids:
            raise ValidationError("Another offer has already been accepted for this property")

    def action_decline_offer(self):
        self.status = 'refused'

        # If all offers have been refused, set the property state to 'received'
        # Just means an offer has been made, but none have been accepted
        # And the selling price is set to 0 because no offers have been accepted
        if all(self.property_id.offer_ids.mapped('status')):
            self.property_id.write({
                'selling_price': 0,
                'state': 'received'
            })

    def extend_offer_deadline(self):
        pass

