from odoo import models, fields,api
from odoo.exceptions import UserError
class HealthPlanProduct(models.Model):
    _name = 'health.plan.product'
    _description = 'Productos Asociados al Plan de Salud'

    plan_id = fields.Many2one('health.plan',string="Plan de Salud",required=True,ondelete='cascade')
    product_id = fields.Many2one('product.template',string="Producto",required=True)
    default_code = fields.Char(related='product_id.default_code',string="Referencia Interna",readonly=True)
    promotion = fields.Char(string="Promoción",required=True)
    product_code = fields.Char(string="Código del proveedor",related='product_id.seller_ids.product_code',readonly=True)

    @api.constrains('product_id', 'plan_id')
    def _check_duplicate_product(self):
        """
        Validacion no duplicar productos.
        """
        for record in self:
            duplicates = self.search([
                ('plan_id', '=', record.plan_id.id),
                ('product_id', '=', record.product_id.id),
                ('id', '!=', record.id) 
            ])
            if duplicates:
                raise UserError(f"El producto '{record.product_id.name}' ya está asociado al plan. No se puede duplicar.")