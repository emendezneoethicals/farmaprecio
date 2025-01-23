""" from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    provider_id = fields.Many2one('res.partner',string="Proveedor",domain=[('is_company', '=', True)])
    promotion = fields.Char(string="Promoción")
 """