# -*- coding: utf-8 -*-
{
    'name': "cwl_module",

    'summary': """Initial Thoughts on Module for Comet""",

    'description': """
        Thoughts on module
    """,

    'author': "Comet Welding ltd.",
    'website': "http://www.cometwelding.ca",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'sale', 'purchase', 'maintenance', 'stock', 'project'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/cwl_quality_ior.xml',
        'views/cwl_safety_incidents.xml',
        'views/cwl_safety_nearmiss.xml',
        'views/cwl_safety_toolbox.xml',
        'views/cwl_safety_hazard.xml',
        'views/cwl_safety_firstaid.xml',
        'views/cwl_config_safetype.xml',
        'views/cwl_config_firsttype.xml',
        'views/cwl_prod_loca.xml',
        'views/report_project_task_label.xml',
        'views/report_product_lot_label.xml',
        'views/report_delivery_label.xml',
        'views/label_declare_report.xml',
        'views/cwl_labels_views.xml',
        'views/cwl_labels_templates.xml',
        'views/material_and_time_entry_view.xml',
        'views/cwl_sequence.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images':[],
}