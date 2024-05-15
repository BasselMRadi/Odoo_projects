from odoo import models, api, fields


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_tech_offer = fields.Boolean(string="Technical Offer")
