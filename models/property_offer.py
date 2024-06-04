from odoo import models, fields


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
