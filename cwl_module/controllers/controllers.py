# -*- coding: utf-8 -*-
from odoo import http

# class CwlModule(http.Controller):
#     @http.route('/cwl_module/cwl_module/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cwl_module/cwl_module/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cwl_module.listing', {
#             'root': '/cwl_module/cwl_module',
#             'objects': http.request.env['cwl_module.cwl_module'].search([]),
#         })

#     @http.route('/cwl_module/cwl_module/objects/<model("cwl_module.cwl_module"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cwl_module.object', {
#             'object': obj
#         })


# CODE FROM cwl_labels
# class CwlLabels(http.Controller):
#     @http.route('/cwl_labels/cwl_labels/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/cwl_labels/cwl_labels/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('cwl_module.listing', {
#             'root': '/cwl_labels/cwl_labels',
#             'objects': http.request.env['cwl_module.cwl_labels'].search([]),
#         })

#     @http.route('/cwl_labels/cwl_labels/objects/<model("cwl_module.cwl_labels"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('cwl_module.object', {
#             'object': obj
#         })