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
    'depends': ['website'], 
    'data': [
        'security/ir.model.access.csv',
        #'views/templates.xml',
        'views/prod_grid.xml',
        'views/store_views.xml',
        'views/website_store_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
        
        ],
        'web.assets_qweb': [
           
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
