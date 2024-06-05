from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import ValidationError


class PropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offers'

    price = fields.Float(string="Price")
    status = fields.Selection([('accepted', 'Accepted'), ('refused', 'Refused')],string='Status')
    # The entity placing the bid/offer will be a customer, but there's an entity in Odoo called res.partner
    # Partners represent people or organisations,
    # so we can use res.partner as our 'customer' instead of making a model for that
    partner_id = fields.Many2one('res.partner', string='Customer')

    # estate.property must be linked to this offer model via the property ID
    property_id = fields.Many2one('estate.property', string='Property')

    # We can compute the deadline of an offer based on when it was made x the validity duration
    validity = fields.Integer(string="Validity") # E.g., '5' as in 'valid for 5 days'
    deadline = fields.Date(string="Deadline", compute='_compute_deadline', inverse='_inverse_deadline')
    creation_date = fields.Date(string="Creation Date")

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
