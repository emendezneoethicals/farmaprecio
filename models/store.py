from odoo import models, fields, api
from odoo.exceptions import UserError
import logging, re, requests
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
    image = fields.Binary(string="Imagen de la Tienda",tracking=True)
    description = fields.Text(string="Descripción",tracking=True)
    latitude = fields.Float(string="Latitud",required=True,tracking=True)
    longitude = fields.Float(string="Longitud",required=True,tracking=True)
    DEPARTAMENTOS = [
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
    department = fields.Selection(selection=DEPARTAMENTOS,string="Departamento",tracking=True)
    municipality = fields.Char(string="Municipio", tracking=True)
    zona = fields.Char(string="Zona",required=True, tracking=True)
    active = fields.Boolean(string="Activo", default=True)

    @api.model
    def action_archive_selected(self):
        for record in self:
            record.active = False


    @api.constrains('zona')
    def _check_zona(self):
        for record in self:
            if not record.zona.isdigit():
                raise UserError("El campo 'Zona' solo permite números enteros.")
            
    @api.constrains('phone')
    def _check_phone(self):
        phone_pattern = re.compile(r'^\+?[1-9]\d{1,14}$') 
        for record in self:
            if not phone_pattern.match(record.phone):
                raise UserError("El campo 'Teléfono' debe contener un número válido. Ejemplo: +50212345678 o 12345678.")        
            
    @api.onchange('municipality')
    def _onchange_municipality(self):
        """Convierte el valor del campo municipio a mayúsculas."""
        if self.municipality:
            self.municipality = self.municipality.upper()

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
                        })

                        _logger.warning(f"Datos guardados: latitud={latitude}, longitud={longitude}, municipio={municipality}, departamento={department}")
                    else:
                        _logger.warning("No se encontraron resultados en la API para esta dirección.")
                else:
                    _logger.warning(f"No se obtuvo una respuesta válida de la API. Código de estado: {response.status_code}")
            except Exception as e:
                _logger.error(f"Error en geocodificación: {e}")

