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
        # groups
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'security/model_access.xml',
        'security/ir_rule.xml',

        'views/property_view.xml',
        'views/property_type_view.xml',
        'views/property_tag_view.xml',
        'views/property_offer_view.xml',
        'views/menu_items.xml',

        # Data Files
        'data/estate.property.tag.csv',

        # Report
        'reports/report_template.xml',
        'reports/property_report.xml',
    ],
    "depends": [
        'base',
        'mail'
    ],
    "assets": {
      "web.assets_backend": [
        "real_estate_ads/static/src/js/my_custom_tag.js",
        "real_estate_ads/static/src/xml/my_custom_tag.xml",
      ]
    },
    "application": True,
    "license": "LGPL-3"
}