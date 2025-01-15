from odoo import http
from odoo.http import request

class Farmaprecio(http.Controller):

    @http.route('/', auth='public', website=True)
    def index(self, **kw):
        return request.render('farmaprecio.homepage')