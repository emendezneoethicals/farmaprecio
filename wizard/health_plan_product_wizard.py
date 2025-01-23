import base64
import pandas as pd
from odoo import models, fields, api

class ImportHealthPlanProductsWizard(models.TransientModel):
    _name = 'import.health.plan.products.wizard'
    _description = 'Importar Productos al Plan de Salud'

    file = fields.Binary(string="Archivo Excel", required=True)
    filename = fields.Char(string="Nombre del Archivo")

    def import_products(self):
        if not self.file:
            raise ValueError("No se ha cargado ningún archivo.")
        data = base64.b64decode(self.file)
        df = pd.read_excel(data)

        # Depuración: Mostrar columnas disponibles
        print("Columnas encontradas en el archivo:", df.columns)

        required_columns = ['Referencia Interna', 'Promoción']
        for column in required_columns:
            if column not in df.columns:
                raise ValueError(f"La columna requerida '{column}' no está presente en el archivo Excel.")

        active_plan_id = self.env.context.get('active_id')
        if not active_plan_id:
            raise ValueError("No se pudo determinar el plan de salud activo.")

        plan = self.env['health.plan'].browse(active_plan_id)

        for _, row in df.iterrows():
            product = self.env['product.template'].search([('default_code', '=', row['Referencia Interna'])], limit=1)
            if not product:
                raise ValueError(f"El producto con referencia interna {row['Referencia Interna']} no existe.")

            self.env['health.plan.product'].create({
                'plan_id': plan.id,
                'product_id': product.id,
                'promotion': row.get('Promoción', '')
            })

