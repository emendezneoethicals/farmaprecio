from odoo import models, fields

class HealthPlanProduct(models.Model):
    _name = 'health.plan.product'
    _description = 'Productos Asociados al Plan de Salud'

    plan_id = fields.Many2one('health.plan',string="Plan de Salud",required=True,ondelete='cascade')
    product_id = fields.Many2one('product.template',string="Producto",required=True)
    default_code = fields.Char(related='product_id.default_code',string="Referencia Interna",readonly=True)
    promotion = fields.Char(string="Promoción")
    product_code = fields.Char(string="Código del proveedor",related='product_id.seller_ids.product_code',readonly=True)
