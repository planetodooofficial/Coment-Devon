from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class timesheet_entry(models.Model):
    _name = 'cwl.module.timesheet.approval'
    _rec_name = 'time_entry_id'

    time_entry_id = fields.Char(string='Time Entry ID', readonly=True, required=True, copy=False, index=True,
                                default=lambda self: _('New'))
    employee_id = fields.Many2one('res.users', 'Employee', default=lambda self: self.env.user.id, readonly=True)
    date = fields.Date('Date', default=fields.Date.today, readonly=True)
    project_id = fields.Many2one('project.project', 'Project')
    task_id = fields.Many2one('project.task', 'Project Task')
    category_timesheet = fields.Selection(
        [('reg', 'Regular'), ('regot', 'Regular OT'), ('port', 'Portable'), ('portot', 'Portable OT'),
         ('stat', 'Stat Holiday'), ('vacnopay', 'Vacation Not Paid'), ('safe', 'Safety'), ('other', 'Other')],
        'Timesheet Category')
    description = fields.Text('Description')
    duration = fields.Float("Duration (Hours)")
    status = fields.Selection([('pending', 'Pending'), ('approved', 'Approved')], default='pending')

    @api.model
    def create(self, vals):
        if vals.get('time_entry_id', _('New')) == _('New'):
            vals['time_entry_id'] = self.env['ir.sequence'].next_by_code('Time_Entry_ID') or _('New')
        result = super(timesheet_entry, self).create(vals)
        return result

    def approve_timesheet(self):
        # group = self.env['res.groups'].search([('name', '=', 'Portal User')])
        # is_desired_group = self.env.user.id in group.users.ids
        # if is_desired_group is True:
        #     raise ValidationError(_("Please contact your system Administration."))
        # else:
        #     pass
        if self.status == 'pending':
            employee = self.env['hr.employee'].search([('user_id', '=', self.employee_id.id)])
            time_sheet = self.env['account.analytic.line'].create({
                'employee_id': employee.id,
                'date': self.date,
                'name': self.description,
                'project_id': self.project_id.id,
                'task_id': self.task_id.id,
                'unit_amount': float(self.duration)
            })
            if time_sheet:
                self.update({
                    'status': 'approved'
                })
        else:
            raise ValidationError(_("Time Entry has already been approved and processed."))

    @api.multi
    def back_to_web(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/employee/portal/'
        }


class Material_Entry(models.Model):
    _name = 'cwl.module.material.approval'
    _rec_name = 'material_entry_id'

    material_entry_id = fields.Char(string='Material Entry ID', readonly=True, required=True, copy=False, index=True,
                                    default=lambda self: _('New'))
    date = fields.Date('Date', default=fields.Date.today, readonly=True)
    employee_id = fields.Many2one('res.users', 'Employee', default=lambda self: self.env.user.id, readonly=True)
    sale_id = fields.Many2one('sale.order', 'Project')
    status = fields.Selection([('pending', 'Pending'), ('approved', 'Approved')], default='pending')
    material_list_ids = fields.One2many('material.list', 'material_list_id', string='List of Materials')
    button_hide = fields.Boolean('Button Hide')

    @api.model
    def create(self, vals):
        if vals.get('material_entry_id', _('New')) == _('New'):
            vals['material_entry_id'] = self.env['ir.sequence'].next_by_code('Material_Entry_ID') or _('New')
        result = super(Material_Entry, self).create(vals)
        return result

    def approve_material(self):
        # group = self.env['res.groups'].search([('name', '=', 'Portal User')])
        # is_desired_group = self.env.user.id in group.users.ids
        # if is_desired_group is True:
        #     raise ValidationError(_("Please contact your system Administration."))
        # else:
        #     pass
        sale_order = self.env['sale.order'].search([('id', '=', self.sale_id.id)])
        if self.status == 'pending':
            for rec in self.material_list_ids:
                sale_order_line = self.env['sale.order.line'].create({
                    'product_id': rec.product_id.id,
                    'name': rec.product_id.description if rec.product_id.description else rec.product_id.name,
                    'product_uom': rec.product_id.uom_id.id,
                    'product_uom_qty': rec.qty,
                    'price_unit': rec.product_id.list_price,
                    'order_id': sale_order.id
                })

            sale_order.action_confirm()

            picking = self.env['stock.picking'].search([('origin', '=', sale_order.name)])
            stock_move = self.env['stock.move'].search([('picking_id', '=', picking.id)])
            for _rec in stock_move:
                stock_move_line = self.env['stock.move.line'].search(
                    [('picking_id', '=', picking.id), ('move_id', '=', _rec.id)])
                if stock_move_line:
                    for record in self.material_list_ids:
                        if record.product_id.name == stock_move_line.product_id.name:
                            stock_move_line.update({
                                'qty_done': record.qty,
                                'lot_id': record.lot_ids if record.lot_ids else False,
                            })
                else:
                    for _record in self.material_list_ids:
                        for prod in picking.move_ids_without_package:
                            if _record.product_id.name == prod.product_id.name:
                                prod.update({
                                    'quantity_done': _record.qty
                                })

            picking.button_validate()

            self.update({
                'status': 'approved'
            })

        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/employee/portal/'
        }

    @api.multi
    def back_to_web(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/employee/portal/'
        }


class ProductOne2many(models.Model):
    _name = 'material.list'

    material_list_id = fields.Many2one('cwl.module.material.approval', 'Material List ID')
    product_id = fields.Many2one('product.product', string='Material')
    lot_ids = fields.Many2one('stock.production.lot', string='Lots/Serial Numbers')
    qty = fields.Float('Quantity Used', default=1.00)
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure')


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order.line'

    lot_id = fields.Many2one('stock.production.lot', string='Lots/Serial Numbers')


class ProjectProjectInherit(models.Model):
    _inherit = 'project.project'

    @api.model
    def create(self, vals):
        result = super(ProjectProjectInherit, self).create(vals)
        if result:
            stage_id=self.env['project.task.type'].sudo().search([])
            for stage in stage_id:
                stage.write({'project_ids':[(4, result.id, None)]})
        return result
