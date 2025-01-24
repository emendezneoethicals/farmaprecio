from odoo import models, fields,api
from odoo.exceptions import UserError
class HealthPlanProduct(models.Model):
    _name = 'health.plan.product'
    _description = 'Productos Asociados al Plan de Salud'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    follower_ids = fields.Many2many('res.users', string='Followers')
    
    plan_id = fields.Many2one('health.plan',string="Plan de Salud",required=True,ondelete='cascade',tracking=True)
    product_id = fields.Many2one('product.template',string="Producto",required=True,tracking=True)
    default_code = fields.Char(related='product_id.default_code',string="Referencia Interna",readonly=True,tracking=True)
    promotion = fields.Char(string="Promoción",required=True,tracking=True)
    product_code = fields.Char(string="Código del proveedor",related='product_id.seller_ids.product_code',readonly=True,tracking=True)

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