from odoo import models, api, fields


class TechnicalOrderLine(models.Model):
    _name = "technical.order.line"
    _description = "Technical Order Line"

    product_id = fields.Many2one('product.product', string='Product', required=True)
    description = fields.Char(string='Description', related="product_id.name")
    quantity = fields.Float(string='Quantity', default=1)
    price = fields.Float(string='Price', readonly=True, related="product_id.list_price")
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    order_id = fields.Many2one('technical.order', string='Order')

    @api.depends("quantity", "price")
    def _compute_total(self):
        for record in self:
            record.total = record.quantity * record.price
