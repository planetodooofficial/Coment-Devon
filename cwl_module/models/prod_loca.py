# -*- coding: utf-8 -*-


from odoo import models, fields, api, _


class cwl_prod_loca(models.Model):
    _inherit = 'product.template'

    prod_loca_id = fields.Many2one('stock.location', string='Product Default Location')

class cwl_move_loca(models.Model):
    _inherit = 'stock.move'

    move_loca_id = fields.Char(string='Invt Location', related='product_id.prod_loca_id.display_name')
        #
        #fields.Many2one('product_id.prod_loca_id', string='Invt Location', readonly=True)
