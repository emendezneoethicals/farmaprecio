from odoo import http
from odoo.http import request
import json

class WebsiteStoreLocation(http.Controller):
    @http.route(['/ubicaciones'], type='http', auth='public', website=True)
    def ubicaciones(self, **kwargs):
         # Lista de departamentos
        departamentos = [
            ('alta_verapaz', 'Alta Verapaz'),
            ('baja_verapaz', 'Baja Verapaz'),
            ('chimaltenango', 'Chimaltenango'),
            ('chiquimula', 'Chiquimula'),
            ('el_progreso', 'El Progreso'),
            ('escuintla', 'Escuintla'),
            ('guatemala', 'Guatemala'),
            ('huehuetenango', 'Huehuetenango'),
            ('izabal', 'Izabal'),
            ('jalapa', 'Jalapa'),
            ('jutiapa', 'Jutiapa'),
            ('peten', 'Petén'),
            ('quetzaltenango', 'Quetzaltenango'),
            ('quiche', 'Quiché'),
            ('retalhuleu', 'Retalhuleu'),
            ('sacatepequez', 'Sacatepéquez'),
            ('san_marcos', 'San Marcos'),
            ('santa_rosa', 'Santa Rosa'),
            ('solola', 'Sololá'),
            ('suchitepequez', 'Suchitepéquez'),
            ('totonicapan', 'Totonicapán'),
            ('zacapa', 'Zacapa'),
        ]

        domain = []

        # Filtros 
        if kwargs.get('zona'):
            domain.append(('zona', 'ilike', kwargs['zona']))
        if kwargs.get('municipality'):
            domain.append(('municipality', 'ilike', kwargs['municipality']))
        if kwargs.get('department'):
            domain.append(('department', '=', kwargs['department']))

        # Obtener las tiendas filtradas
        stores = request.env['store'].sudo().search(domain)

        return request.render('farmaprecio.website_ubicaciones', {
            'stores_json': json.dumps([{
                'name': store.name,
                'zona': store.zona,
                'opening_hours': store.opening_hours,
                'address': store.address,
                'phone': store.phone,
                'latitude': store.latitude,
                'longitude': store.longitude,
                'municipality': store.municipality,
                'department': store.department,
            } for store in stores]),
            'departamentos': departamentos,
        })
