from odoo import models, api, fields
from odoo.exceptions import ValidationError


class TechnicalOrder(models.Model):
    _name = "technical.order"
    _description = "Technical Order"
    _rec_name="sequence"
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']

    sequence = fields.Char(string='Sequence')
    request_name = fields.Char(string='Request Name', required=True)
    requested_by_id = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user, required=True)
    customer_id = fields.Many2one('res.partner', string='Customer', domain="[('is_tech_offer', '=', True)]", required=True)
    start_date = fields.Date(string='Start Date', default=fields.Date.today, required=True)
    end_date = fields.Date(string='End Date')
    rejection_reason = fields.Text(string="Rejection Reason", states={"draft": [("invisible", False)]}, readonly=True)
    order_lines = fields.One2many('technical.order.line', 'order_id', string='Order Lines')
    total_price = fields.Float(string='Total', compute='_compute_total_price', store=True)
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submit_for_approval', 'Submit for Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled')],
         string='Status', default='draft',copy=False, index=True, track_visibility='onchange')

    sale_order_ids = fields.Many2many(comodel_name="sale.order",string="Sale Order",copy=False, index=True,)

    sale_count = fields.Integer(string="SO Count",compute='compute_sale_count')

    @api.depends('sale_order_ids')
    def compute_sale_count(self):
        for rec in self:
            rec.sale_count=len(rec.sale_order_ids)

    @api.depends('order_lines.total')
    def _compute_total_price(self):
        for order in self:
            order.total_price = sum(order.order_lines.mapped("total"))

    # def action_draft

    def action_draft(self):
        self.write({'status': 'draft'})

    def action_submit(self):
        self.write({'status': 'submit_for_approval'})

    def action_approve(self):
        mail_content = "  Technical Order  " + str(self.sequence) + " Has Been Approved"

        sale_manager=self.env.ref('technical_order_module.group_sale_manager_technical_order')
        if sale_manager:
            for user in sale_manager.users:
                main_content = {
                    'subject': _('Technical Order'),
                    'author_id': self.env.user.partner_id.id,
                    'body_html': mail_content,
                    'email_to': user.email,
                }
                self.env['mail.mail'].create(main_content).send()

        self.write({'status': 'approved'})

    def action_reject(self):
        self.write({'status': 'rejected'})

    def action_cancel(self):
        self.write({'status': 'cancelled'})

    def action_reset_to_draft(self):
        self.write({'status': 'draft'})

    @api.model
    def create(self, vals):
        res = super(TechnicalOrder, self).create(vals)
        res.sequence = self.env['ir.sequence'].next_by_code('technical_order_seq')
        return res

    @api.constrains('order_lines')
    def check_validation(self):
        if not self.order_lines:
            raise ValidationError("Please Enter Order Lines")

    def create_so(self):
        order_line=[]
        for order in self.order_lines:
            order_line.append((0,0,{
                'product_id':order.product_id.id,
                'product_uom_qty':order.quantity,
                'price_unit':order.price,
            }))

        self.sale_order_ids += self.env['sale.order'].create({
            'partner_id': self.customer_id.id,
            'order_line': order_line
        })

    def action_view_sale_order(self):
        return {
            'name': _('Sale Order'),
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', self.sale_order_ids.ids)],
            'type': 'ir.actions.act_window',
        }

