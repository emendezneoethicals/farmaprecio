from odoo import models, fields, api
import logging
import requests
_logger = logging.getLogger(__name__)

class Store(models.Model):
    _name = 'store'
    _description = 'Store'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    follower_ids = fields.Many2many('res.users', string='Followers')

    name = fields.Char(string="Nombre", required=True, tracking=True)
    address = fields.Char(string="Direccion",required=True,tracking=True)
    phone = fields.Char(string="Telefono",required=True,tracking=True)
    opening_hours = fields.Char(string="Horario de Apertura",required=True,tracking=True)
    image = fields.Binary(string="Imagen de la Tienda",required=True,tracking=True)
    description = fields.Text(string="Descripción",required=True,tracking=True)
    latitude = fields.Float(string="Latitud",required=True,tracking=True)
    longitude = fields.Float(string="Longitud",required=True,tracking=True)
    department = fields.Char(string="Departamento",required=True, tracking=True)
    municipality = fields.Char(string="Municipio",required=True, tracking=True)
    zona = fields.Integer(string="Zona",required=True, tracking=True)


    @api.onchange('address')
    def _compute_geolocation(self):
        if not self.address:
            self.write({
                'latitude': False,
                'longitude': False,
                'department': False,
                'municipality': False
            })
            _logger.warning("Direccion Vacia")
            return
                  
        if self.address:
            _logger.warning(f"Iniciando geocodificación para la dirección: {self.address}")
            try:
                api_key = "AIzaSyCcAZQka1gsjE3vtrrNVwQzzfMVAU0_V1A"  
                url = f"https://maps.googleapis.com/maps/api/geocode/json?address={self.address}&key={api_key}"
                response = requests.get(url)
                _logger.warning(f"Respuesta de Google Maps API: {response.status_code}")

                if response.status_code == 200:
                    data = response.json()
                    _logger.debug(f"Datos recibidos de la API: {data}")

                    if data['results']:
                        # Guardar latitud, longitud, departamento y municipio
                        location = data['results'][0]['geometry']['location']
                        latitude = location['lat']
                        longitude = location['lng']

                        department = ""
                        municipality = ""
                        for component in data['results'][0]['address_components']:
                            if 'administrative_area_level_2' in component['types']:
                                municipality = component['long_name']
                                _logger.info(f"Municipio detectado: {municipality}")
                            if 'administrative_area_level_1' in component['types']:
                                department = component['long_name']
                                _logger.info(f"Departamento detectado: {department}")

                        # Guardar los datos en la base de datos
                        self.write({
                            'latitude': latitude,
                            'longitude': longitude,
                            'department': department,
                            'municipality': municipality
                        })

                        _logger.warning(f"Datos guardados: latitud={latitude}, longitud={longitude}, municipio={municipality}, departamento={department}")
                    else:
                        _logger.warning("No se encontraron resultados en la API para esta dirección.")
                else:
                    _logger.warning(f"No se obtuvo una respuesta válida de la API. Código de estado: {response.status_code}")
            except Exception as e:
                _logger.error(f"Error en geocodificación: {e}")

