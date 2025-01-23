{
    'name': 'FarmaPrecio',
    'version': '1.0',
    'summary': 'Replica del sitio web FarmaPrecio en Odoo 16',
    'description': """
        Este módulo implementa una página web personalizada para FarmaPrecio,
        desarrollada en Odoo 16 Community Edition.
    """,
    'author': 'Angel Mendez',
    'website': '',
    'category': 'Website',
    'license': 'LGPL-3',
    'depends': ['base','website','website_sale'], 
    'data': [
        'security/ir.model.access.csv',
        #'views/templates.xml',
        'views/prod_grid.xml',
        'views/store_views.xml',
        'views/website_store_templates.xml',
        'views/website_store_location.xml',
        'views/website_config_settings_view.xml',
        'views/healt_plan_views.xml',
        'views/product_template_views.xml',
        
    ],
    'assets': {
        'web.assets_frontend': [
            "farmaprecio/static/src/js/store_map.js",
        
            
        
        ],
        'web.assets_qweb': [
           
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
