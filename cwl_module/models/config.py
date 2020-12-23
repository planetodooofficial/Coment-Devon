
# -*- coding: utf-8 -*-


from odoo import models, fields


class cwl_conf_safe_type(models.Model):
    _name = 'cwl.module.conf.safe.type'
    _rec_name = 'conf_type_name'
    _order = 'conf_type_name'

    conf_type_name = fields.Char(string='Type Name', required=True, copy=False, index=True)

class cwl_conf_safe_first_type(models.Model):
        _name = 'cwl.module.conf.safe.firsttype'
        _rec_name = 'conf_firsttype_name'
        _order = 'conf_firsttype_name'

        conf_firsttype_name = fields.Char(string='First Aid Type Name', required=True, copy=False, index=True)