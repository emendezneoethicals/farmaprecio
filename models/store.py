from odoo import models, fields

class Store(models.Model):
    _name = 'store'
    _description = 'Store'

    name = fields.Char(string="Nombre", required=True)
    address = fields.Char(string="Direccion")
    phone = fields.Char(string="Telefono")
    opening_hours = fields.Char(string="Horario de Apertura")
    image = fields.Binary(string="Imagen de la Tienda")
    description = fields.Text(string="Descripción")
