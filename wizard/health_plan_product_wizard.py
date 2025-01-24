import base64
import pandas as pd
from odoo import models, fields, api
from odoo.exceptions import UserError

class ImportHealthPlanProductsWizard(models.TransientModel):
    _name = 'import.health.plan.products.wizard'
    _description = 'Importar Productos al Plan de Salud'

    file = fields.Binary(string="Archivo Excel", required=True)
    filename = fields.Char(string="Nombre del Archivo")

    def import_products(self):
        if not self.file:
            raise UserError("No se ha cargado ningún archivo.")
        
        data = base64.b64decode(self.file)
        df = pd.read_excel(data)

        required_columns = ['Referencia Interna', 'Promoción']
        for column in required_columns:
            if column not in df.columns:
                raise UserError(f"La columna requerida '{column}' no está presente en el archivo Excel.")

        active_plan_id = self.env.context.get('active_id')
        if not active_plan_id:
            raise UserError("No se pudo determinar el plan de salud activo.")

        plan = self.env['health.plan'].browse(active_plan_id)

        errors = []
        for index, row in df.iterrows():
            # Validar que las celdas no estén vacías
            if pd.isna(row['Referencia Interna']) or pd.isna(row['Promoción']):
                errors.append(f"Fila {index + 2}: Falta 'Referencia Interna' o 'Promoción'.")
                continue

            product = self.env['product.template'].search([('default_code', '=', row['Referencia Interna'])], limit=1)
            if not product:
                errors.append(f"Fila {index + 2}: El producto con referencia interna '{row['Referencia Interna']}' no existe.")
                continue

            # Crear el registro si no hay problemas
            self.env['health.plan.product'].create({
                'plan_id': plan.id,
                'product_id': product.id,
                'promotion': row['Promoción']
            })

        # Si hay errores, lanzar una excepción
        if errors:
            error_message = "Errores encontrados al procesar el archivo Excel:\n" + "\n".join(errors)
            raise UserError(error_message)
