from odoo import models, fields, api
from datetime import timedelta


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
            rec.validity = (rec.deadline - rec.creation_date).days # They're date objects, so have access to 'days' attribute

