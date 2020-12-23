# -*- coding: utf-8 -*-


from odoo import models, fields, api, _


class cwl_quality_ior(models.Model):
    _name = 'cwl.module.quality.ior'
    _rec_name = 'ior_id'

    ior_id = fields.Char(string='IOR ID', readonly=True, required=True, copy=False, index=True,
                         default=lambda self: _('New'))
    ior_open_date = fields.Date(string="Date Opened", default=fields.Date.today())
    # recorder_id = fields.Many2one('hr.employee', 'employee_id', string='Recorded by')
    # employee_id = fields.Many2one('hr.employee', string='Employee')
    ior_so_id = fields.Many2one('sale.order', string='Sale Order/Project ID')
    ior_recorder = fields.Many2one('hr.employee', string='Recorded by')         # fields.Char(string='Recorded by')                    #<!--PLANET ODOO: many2one = hr.Employee.Employee ID -->
    ior_type = fields.Selection([
        ('nn', 'Non-Conformance'),
        ('cc', 'Customer Complaint'),
        ('ia', 'Internal Audit'),
        ('io', 'Improvement Opportunity')], string='IOR Type')
    ior_prob_type = fields.Selection([
        ('lod', 'Lack of Documentation'),
        ('fe', 'Fabrication Error'),
        ('ee', 'Engineering Error'),
        ('ie', 'Install Error'),
        ('dp', 'Damaged Parts'),
        ('ivt', 'Lack/Wrong Inventor'),
        ('jp', 'Inadequate Job Prep'),
        ('dc', 'Document Change'),
        ('ot', 'Other')], string='Problem Type')
    ior_prob_cause = fields.Selection([
        ('de', 'Document Error'),
        ('pe', 'Procedure Error'),
        ('he', 'Human Error'),
        ('sp', 'Supplier Error'),
        ('em', 'Equipment Malfunction'),
        ('ir', 'Incorrect Recordkeeping'),
        ('lg', 'Logistic Error'),
        ('ot', 'Other')], string='Problem Cause')
    ior_dept = fields.Selection([
        ('ad', 'Administration'),
        ('op', 'Operations'),
        ('pu', 'Purcahsing'),
        ('sa', 'Safety'),
        ('mg', 'Management')], string='Department')
    department_id = fields.Many2one('hr.department', string='Department')
    ior_prod_id = fields.Char(string='Product ID')
    product_id = fields.Many2one('product.product', string='Product ID')
    ior_prod_serial = fields.Char(string='Prod SN/Lot ID')              #<!-- PLANET ODOO: Lot/Serial Number based on part number above
    # ior_supplier = fields.Char(string='Supplier Name')
    partner_id = fields.Many2one('res.partner', string='Partner ID')
    ior_purch_order = fields.Many2one('purchase.order', string='Purchase Order')                                                # PLANET ODOO: Add link to Purchase orders
    ior_prod_qty = fields.Integer(string='Product Qty')
    ior_prob_desc = fields.Text(string='Problem Description')
    ior_prob_exp = fields.Text(string='Problem Explanation')
    ior_prob_corr = fields.Text(string='Problem Corrective Action')
    ior_prob_disp = fields.Selection([
        ('rw', 'Rework'),
        ('ac', 'Accepted'),
        ('rj', 'Rejected/Scrapped'),
        ('rp', 'Repair')], string='Problem Disposition')
    ior_disp_appr = fields.Many2one('hr.employee', string='Approved by')                   #<!--PLANET ODOO: many2one = hr.Employee.Employee ID -->
    ior_disp_ver = fields.Text(string='Effectiveness')
    ior_prev_act = fields.Text(string='Preventative Action')
    ior_prev_ver = fields.Text(string='Effectiveness')
    ior_prev_date = fields.Date(string="Followup Date")
    ior_prev_pers = fields.Many2one('hr.employee', string='Followup By')                   #<!--PLANET ODOO: many2one = hr.Employee.Employee ID -->
    ior_cost_rewk = fields.Monetary(currency_field='company_currency', string='Cost of Rework')
    # PLANET ODOO: Change to fields.Monetary
    ior_cost_frei = fields.Monetary(currency_field='company_currency', string='Cost of Freight')
    # PLANET ODOO: Change to fields.Monetary
    ior_cost_labo = fields.Monetary(currency_field='company_currency', string='Cost of Labour')
    # PLANET ODOO: Change to fields.Monetary
    ior_cost_cred = fields.Monetary(currency_field='company_currency', string='Cost of Customer Credit')
    # PLANET ODOO: Change to fields.Monetary
    ior_cost_total = fields.Monetary(currency_field='company_currency', string='Total Cost')
    # PLANET ODOO: sum of above 4 fields to this one
    ior_final_sign = fields.Many2one('hr.employee', string='Manager Sign-off')             #<!--PLANET ODOO: many2one = hr.Employee.Employee ID -->
    ior_final_date = fields.Date(string='Sign-off Date')
    company_id = fields.Many2one('res.company', string='Company', index=True,
                                 default=lambda self: self.env.user.company_id.id)
    company_currency = fields.Many2one(string='Currency', related='company_id.currency_id', readonly=True,
                                       relation="res.currency")
    ior_state = fields.Selection([
        ('open', 'Open'),
        ('done', 'Done')],
        string='Status', readonly=True, default='open')

    @api.model
    def create(self, vals):
        if vals.get('ior_id', _('New')) == _('New'):
            vals['ior_id'] = self.env['ir.sequence'].next_by_code('Quality_IRO_ID') or _('New')
        result = super(cwl_quality_ior, self).create(vals)
        return result

    @api.onchange('ior_cost_rewk', 'ior_cost_frei', 'ior_cost_labo', 'ior_cost_cred')
    def total_cost(self):
        if self.ior_cost_rewk or self.ior_cost_frei or self.ior_cost_labo or self.ior_cost_cred:
            self.ior_cost_total = self.ior_cost_rewk + self.ior_cost_frei + self.ior_cost_labo + self.ior_cost_cred

    def action_state_done(self):
        for rec in self:
            rec.ior_state = 'done'

    def action_state_open(self):
        for rec in self:
            rec.ior_state = 'open'

    @api.multi
    def back_to_web(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/employee/portal/'
        }


