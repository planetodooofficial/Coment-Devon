# -*- coding: utf-8 -*-
import json
import re
from datetime import date

from odoo import fields, http, tools, _
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class EmployeePortal(http.Controller):

    @http.route('/employee/portal/', type="http", auth="public", website=True, csrf=False)
    def retrieve_data(self, **kw):
        return request.render('employee_portal.employee_portal')

    @http.route('/employee/timeentry/', type="http", auth="user", website=True, csrf=False)
    def employee_form(self, **kw):
        project_ids = []

        project = http.request.env['project.project'].sudo().search([])
        for ids in project:
            project_ids.append(ids)

        project_values = {
            'projects': project_ids,
            'employee': request.env.user.name,
            'date': date.today(),
        }

        return request.render('employee_portal.employee_timesheet_form', project_values)

    @http.route('/onchange/project_task/', type="http", auth="user", website=True, csrf=False)
    def onchange_task(self, **kw):
        project_task_ids = []
        proj_id = kw.get('project')
        if proj_id:
            project_search = http.request.env['project.task'].sudo().search([('project_id', '=', int(proj_id))])
            for task in project_search:
                project_task_ids.append({
                    'id': task.id,
                    'value': task.name
                })
        return json.dumps(project_task_ids)

    @http.route('/employee/timesheet/submit/', type="http", auth="user", website=True, csrf=False)
    def timesheet_values_to_backend(self, **kw):
        project_id = kw.get('project')
        search_project = http.request.env['project.project'].sudo().search([('id', '=', project_id)])
        task_id = kw.get('task_id')
        search_task = http.request.env['project.task'].sudo().search([('id', '=', task_id)])
        time_entry = request.env['cwl.module.timesheet.approval'].create({
            'employee_id': request.env.user.id,
            'date': date.today(),
            'project_id': search_project.id,
            'task_id': search_task.id,
            'category_timesheet': kw.get('category_id'),
            'description': kw.get('description'),
            'duration': float(kw.get('duration'))
        })
        return request.render('employee_portal.employee_timesheet_form_filled')

    @http.route('/employee/material/submit/', type="http", auth="user", website=True, csrf=False)
    def material_values_to_backend(self, **kw):
        sale_id = kw.get('project')
        prod_id = request.httprequest.form.getlist('product_id')
        lot_id = request.httprequest.form.getlist('lot_id')
        product = []
        lots = []

        search_sale = http.request.env['sale.order'].sudo().search([('id', '=', sale_id)])
        for ids in prod_id:
            product_search = http.request.env['product.template'].sudo().search([('id', '=', ids)]).id
            product.append(product_search)
        for ids in lot_id:
            lot = http.request.env['stock.production.lot'].sudo().search([('id', '=', ids)]).id
            lots.append(lot)

        material_entry = request.env['cwl.module.material.approval'].create({
            'employee_id': request.env.user.id,
            'date': date.today(),
            'sale_id': search_sale.id,
            'product_id': [(6, 0, product)],
            'lot_id': [(6, 0, lots)],
            'qty': float(kw.get('qty'))
        })

        return request.render('employee_portal.employee_material_submit')

    @http.route('/employee/timesheet/view/', type="http", auth="user", website=True, csrf=False)
    def timesheet_view(self, **kw):
        search_employee = http.request.env['hr.employee'].sudo().search([('user_id', '=', request.env.user.id)],
                                                                        limit=1).id
        search_timesheet = http.request.env['cwl.module.timesheet.approval'].sudo().search(
            [('date', '=', date.today()), ('employee_id', '=', request.env.user.id)])
        timesheet_ids = []
        for rec in search_timesheet:
            timesheet_ids.append(rec)
        timesheet_vals = {
            'timesheets': timesheet_ids
        }
        return request.render('employee_portal.employee_timesheet_view', timesheet_vals)

    @http.route('/employee/material/entry/', type="http", auth="user", website=True, csrf=False)
    def material_entry(self, **kw):
        project_ids = []
        project_task_ids = []
        product_ids = []

        project = http.request.env['sale.order'].sudo().search([])
        for ids in project:
            project_ids.append(ids)

        project_task = http.request.env['project.task'].sudo().search([])
        for task_ids in project_task:
            project_task_ids.append(task_ids)

        products = http.request.env['product.template'].sudo().search([])
        for product in products:
            product_ids.append(product)

        material_values = {
            'projects': project_ids,
            'employee': request.env.user.name,
            'date': date.today(),
            'project_task': project_task_ids,
            'product_ids': product_ids
        }
        return request.render('employee_portal.employee_material_entry_form', material_values)

    @http.route('/product/search_by/barcode/', type="http", auth="user", website=True, csrf=False)
    def product_by_partid(self, **kw):

        products_by_barcode = {}
        barcode_products = []
        stock_loc = ''
        stock_loc_list = []

        barcode = kw.get('search_products')

        if barcode:
            barcodes = http.request.env['product.template'].sudo().search([('barcode', '=', barcode)])
            stock_loc = http.request.env['stock.quant'].sudo().search([('product_id.name', '=', barcodes.name)])
            for quant in stock_loc:
                if quant.location_id.name != 'Inventory adjustment':
                    stock_loc_list.append(quant)

            if barcodes:
                for products_barcode in barcodes:
                    barcode_products.append(products_barcode)
                    products_by_barcode = {
                        'products_barcode': barcode_products,
                        'stock_loc': stock_loc_list
                    }

        return request.render('employee_portal.product_searchby_barcode', products_by_barcode)

    @http.route('/product/search_by/description/', type="http", auth="user", website=True, csrf=False)
    def search_by_description(self, **kw):

        products_by_name = {}
        description_products = []
        search = kw.get('search_products')

        stock_loc_list = []

        domain = request.website.sale_product_domain()

        domain += [
            '|', '|', '|', ('name', 'ilike', search), ('description', 'ilike', search),
            ('description_sale', 'ilike', search), ('product_variant_ids.default_code', 'ilike', search)]

        if search:
            product_template = http.request.env['product.template']
            search_product = product_template.search(domain)
            stock_loc = http.request.env['stock.quant'].sudo().search([('product_id.name', '=', search)])
            for quant in stock_loc:
                if quant.location_id.name != 'Inventory adjustment':
                    stock_loc_list.append(quant)
            for products_name in search_product:
                description_products.append(products_name)
                products_by_name = {
                    'products_name': description_products,
                    'stock_loc': stock_loc_list
                }

        return request.render('employee_portal.product_searchby_desc', products_by_name)

    @http.route('/product/search_by/location/', type="http", auth="user", website=True, csrf=False)
    def search_by_location(self, **kw):
        products_by_location = {}
        location_products = []
        location = kw.get('search_products')

        if location:
            locations = http.request.env['stock.quant'].sudo().search([('location_id.name', '=', location)])
            if locations:
                for products_location in locations:
                    location_products.append(products_location)
                    products_by_location = {
                        'products_location': location_products
                    }
        return request.render('employee_portal.product_searchby_location', products_by_location)

    @http.route('/product/search_by/lot/', type="http", auth="user", website=True, csrf=False)
    def search_by_lot(self, **kw):
        products_by_lot = {}
        lot_products = []
        stock_loc_list = []
        lot = kw.get('search_products')

        if lot:
            lots = http.request.env['stock.production.lot'].sudo().search(
                [('name', '=', lot)])
            stock_loc = http.request.env['stock.quant'].sudo().search([('product_id.name', '=', lots.product_id.name)])
            for quant in stock_loc:
                if quant.location_id.name != 'Inventory adjustment':
                    stock_loc_list.append(quant)

            if lots:
                for products_lot in lots:
                    lot_products.append(products_lot)
                    products_by_lot = {
                        'products_lot': lot_products,
                        'stock_loc': stock_loc_list
                    }

        return request.render('employee_portal.product_searchby_lot', products_by_lot)

    @http.route('/onchange/product_lotID/', type="http", auth="user", website=True, csrf=False)
    def onchange_product_lot(self, **kw):
        list_lot_ids = []
        product_id = request.httprequest.form.getlist('product')
        if product_id:
            for prod_id in product_id:
                product_template = http.request.env['product.template'].sudo().search([('id', '=', prod_id)])
                product_variant = http.request.env['product.product'].sudo().search([('name', '=', product_template.name)])
                product_search = http.request.env['stock.production.lot'].sudo().search(
                    [('product_id.name', '=', product_variant.name)])
                for product in product_search:
                    list_lot_ids.append({
                        'id': product.id,
                        'value': product.name
                    })
        return json.dumps(list_lot_ids)
