{
    "name": "Real Estate Ads",
    "version": "1.0",
    "author": "Jake",
    "website": "https://www.example.com",
    "description": "Real Estate Ads to show available properties",
    "installable": True, # Will always be true, whether you add it or not
    "category": "Sales",
    # Security policies, views, and data files all go in here
    "data": [
        'security/ir.model.access.csv',
        'views/property_view.xml', # we load this one first, because it contains an import for the menu_items action
        'views/menu_items.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'data/property_type.xml',
        'data/estate.property.tag.csv'
    ],
    "depends": [
        'base'
    ],
    "application": True,
    "license": "LGPL-3"
}