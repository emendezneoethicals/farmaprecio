from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)   
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    show_prices = fields.Boolean(
        string='Mostrar precios',
        default=lambda self: self._default_show_prices(),
    )

    @api.model
    def _default_show_prices(self):
        """Obtén el valor predeterminado del config_parameter."""
        return self.env['ir.config_parameter'].sudo().get_param(
            'website.show_prices', default='True') == 'True'

    @api.model
    def get_values(self):
        """Carga los valores desde ir.config_parameter."""
        res = super(ResConfigSettings, self).get_values()
        res.update(
            show_prices=self.env['ir.config_parameter'].sudo().get_param(
                'website.show_prices', default='True') == 'True',
        )
        return res

    @api.model
    def set_values(self):
        """Guarda los valores en ir.config_parameter."""
        super(ResConfigSettings, self).set_values()
        self.env['ir.config_parameter'].sudo().set_param(
            'website.show_prices', str(self.show_prices)
        )

        