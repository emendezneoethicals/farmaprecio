from odoo import models, fields,api

class HealthPlan(models.Model):
    _name = 'health.plan'
    _description = 'Plan de Salud'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    follower_ids = fields.Many2many('res.users', string='Followers')
    name = fields.Char(string="Nombre del Plan", required=True,tracking=True)
    provider_id = fields.Many2one('res.partner',string="Proveedor",required=True, domain=[('is_company', '=', True)],tracking=True)
    logo = fields.Binary(related='provider_id.image_1920',string="Logo del Proveedor",readonly=True,tracking=True)
    product_ids = fields.One2many('health.plan.product','plan_id',string="Productos Asociados",tracking=True)