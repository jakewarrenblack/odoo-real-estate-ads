{
    "name": "Real Estate Ads",
    "version": "1.0",
    "author": "Jake",
    "website": "https://www.example.com",
    "description": "Real Estate Ads to show available properties",
    "installable": True, # Will always be true, whether you add it or not
    "category": "Sales",
    "data": [
        'security/ir.model.access.csv',
        'views/property_view.xml', # we load this one first, because it contains an import for the menu_items action
        'views/menu_items.xml',
        'views/property_type_view.xml'
    ],
    "depends": [],
    "application": True,
    "license": "LGPL-3"
}