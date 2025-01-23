from odoo import http
from odoo.http import request

class WebsiteStore(http.Controller):
    @http.route(['/nuestras-tiendas'], type='http', auth='public', website=True)
    def nuestras_tiendas(self, **kwargs):
        stores = request.env['store'].sudo().search([])
        return request.render('farmaprecio.website_nuestras_tiendas', {
            'stores': stores,
        })
    
class CustomController(http.Controller):
    @http.route('/', auth='public', website=True)
    def homepage_redirect(self, **kwargs):
        return request.redirect('https://emilio.neoethicals.org/home')
    

