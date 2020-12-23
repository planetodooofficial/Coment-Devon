# -*- coding: utf-8 -*-


from odoo import models, fields, api, _


class cwl_safety_nearmiss(models.Model):
    _name = 'cwl.module.safety.nearmiss'
    _rec_name = 'nearmiss_id'

    nearmiss_id = fields.Char(string='Near Miss ID', readonly=True, required=True, copy=False, index=True,
                         default=lambda self: _('New'))
    nearmiss_date = fields.Date(string="Date", default=fields.Date.today())
    nearmiss_recorder = fields.Char(string='Recorded by')
    nearmiss_empl_post = fields.Char(string='Employee Position', related='employee_id.job_id.name', readonly='1')
    nearmiss_desc = fields.Text(string='Description')
    nearmiss_corr = fields.Text(string='Corrective Action')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    nearmiss_type = fields.Many2one('cwl.module.conf.safe.type', string='Near Miss Type')


    @api.model
    def create(self, vals):
        if vals.get('nearmiss_id', _('New')) == _('New'):
            vals['nearmiss_id'] = self.env['ir.sequence'].next_by_code('Safety_Nearmiss_ID') or _('New')
        result = super(cwl_safety_nearmiss, self).create(vals)
        return result

    @api.multi
    def back_to_web(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/employee/portal/'
        }


class cwl_safety_toolbox(models.Model):
    _name = 'cwl.module.safety.toolbox'
    _rec_name = 'toolbox_id'

    toolbox_id = fields.Char(string='Toolbox Talk ID', readonly=True, required=True, copy=False, index=True,
                         default=lambda self: _('New'))
    toolbox_date = fields.Date(string="Date", default=fields.Date.today())
    toolbox_presentor = fields.Char(string='Presenter')
    toolbox_topic = fields.Char(string='Topic Title')
    toolbox_desc = fields.Text(string='Description of Discussion')
    toolbox_unit = fields.Many2one('maintenance.equipment', string='Equipment ID')
    employee_id = fields.Many2one('hr.employee', string='Employee')


    @api.model
    def create(self, vals):
        if vals.get('toolbox_id', _('New')) == _('New'):
            vals['toolbox_id'] = self.env['ir.sequence'].next_by_code('Safety_Toolbox_ID') or _('New')
        result = super(cwl_safety_toolbox, self).create(vals)
        return result

    @api.multi
    def back_to_web(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/employee/portal/'
        }


class cwl_safety_hazard(models.Model):
    _name = 'cwl.module.safety.hazard'
    _rec_name = 'hazard_id'

    hazard_id = fields.Char(string='Hazard ConditionID', readonly=True, required=True, copy=False, index=True,
                         default=lambda self: _('New'))
    hazard_date = fields.Date(string="Date", default=fields.Date.today())
    hazard_pers = fields.Many2one('hr.employee', string='Reported By')
    hazard_class = fields.Selection([
        ('minor', 'Minor'), ('serious', 'Serious'), ('perm', 'Permanent')], string='Hazard Condition Class')
    hazard_desc = fields.Char(string='Description of Condition')
    hazard_loca = fields.Char(string='Location')
    hazard_act = fields.Text(string='Immediate Action Taken')
    hazard_rec = fields.Text(string='Recommendations')
    hazard_corr = fields.Text(string='Corrective Action')
    hazard_corr_pers = fields.Many2one('hr.employee', string='Corrective Action By')
    hazard_corr_date = fields.Date(string="Completed Date")
    hazard_rep_comm = fields.Text(string='Safety Rep Comments')
    hazard_rep_pers = fields.Many2one('hr.employee', string='Safety Rep')
    hazard_rep_date = fields.Date(string="Comment Date")
    hazard_mgr_comm = fields.Text(string='Manager Comments')
    hazard_mgr_pers = fields.Many2one('hr.employee', string='Manager')
    hazard_mgr_date = fields.Date(string="Comment Date")
    hazard_state = fields.Selection([
        ('open', 'Open'),
        ('done', 'Done')],
        string='Status', readonly=True, default='open')
    hazard_type = fields.Many2one('cwl.module.conf.safe.type', string='Hazard Type')


    @api.model
    def create(self, vals):
        if vals.get('hazard_id', _('New')) == _('New'):
            vals['hazard_id'] = self.env['ir.sequence'].next_by_code('Safety_Hazard_ID') or _('New')
        result = super(cwl_safety_hazard, self).create(vals)
        return result

    def action_state_done(self):
        for rec in self:
            rec.hazard_state = 'done'

    def action_state_open(self):
        for rec in self:
            rec.hazard_state = 'open'

    @api.multi
    def back_to_web(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/employee/portal/'
        }

class cwl_safety_first_aid(models.Model):
    _name = 'cwl.module.safety.firstaid'
    _rec_name = 'firstaid_id'

    firstaid_id = fields.Char(string='First Aid ID', readonly=True, required=True, copy=False, index=True,
                         default=lambda self: _('New'))
    firstaid_empl = fields.Many2one('hr.employee', string='Reported By')
    firstaid_empl_post = fields.Char(string='Employee Position', related='firstaid_empl.job_id.name', readonly='1')
    firstaid_date_occr = fields.Datetime(string="Date Occurred",)  # default=fields.Date.today())
    firstaid_date_rept = fields.Datetime(string="Date Reported",)  # default=fields.Date.today())
    firstaid_desc = fields.Char(string='Description of First Aid')
    firstaid_locat = fields.Char(string='Location of First Aid')
    firstaid_cause = fields.Text(string='Cause of First Aid')
    firstaid_prov = fields.Selection([
        ('yes', 'Yes'), ('no', 'No')], string='Was First Aid Provided')
    firstaid_prov_desc = fields.Char(string='First Aid Provided:')
    firstaid_aider = fields.Many2one('hr.employee', string='Provided By')
    firstaid_copy = fields.Selection([
        ('yes', 'Yes'), ('no', 'No')], string='Copy given to Employee')
    firstaid_type = fields.Many2one('cwl.module.conf.safe.firsttype', string='Type')

    @api.model
    def create(self, vals):
        if vals.get('firstaid_id', _('New')) == _('New'):
            vals['firstaid_id'] = self.env['ir.sequence'].next_by_code('Safety_FirstAid_ID') or _('New')
        result = super(cwl_safety_first_aid, self).create(vals)
        return result

    @api.multi
    def back_to_web(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/employee/portal/'
        }


class cwl_safety_incident(models.Model):
    _name = 'cwl.module.safety.incident'
    _rec_name = 'incident_id'

    incident_id = fields.Char(string='Incident ID', readonly=True, required=True, copy=False, index=True,
                         default=lambda self: _('New'))
    incident_empl = fields.Many2one('hr.employee', string='Employee')
    indident_empl_post = fields.Char(string='Employee Position', related='incident_empl.job_id.name', readonly='1')
    incident_date_occr = fields.Datetime(string="Date Occurred",)  # default=fields.Date.today())
    incident_locat = fields.Char(string='Location of incident')
    incident_equip = fields.Char(string='Equipment Involved')
    incident_type = fields.Selection([
        ('fatality', 'Fatality'),
        ('lti', 'Lost Time'),
        ('medical', 'Medical Aid'),
        ('firstaid', 'First Aid'),
        ('none', 'None')], string='Injury Type')
    incident_prop = fields.Selection([
        ('yes', 'Yes'), ('no', 'No')], string='Property Damage')
    incident_prevent = fields.Selection([
        ('yes', 'Yes'), ('no', 'No')], string='Preventable')
    incident_invest = fields.Selection([
        ('yes', 'Yes'), ('no', 'No')], string='Investigation Required')
    incident_desc = fields.Text(string='Incident Description')
    incident_wit = fields.Many2one('hr.employee', string='Witness')
    incident_wit_comm = fields.Text(string='Witness Comments')
    incident_sup = fields.Many2one('hr.employee', string='Supervisor')
    incident_sup_comm = fields.Text(string='Supervisor Comments')
    incident_corr = fields.Text(string='Corrective Action')

    @api.model
    def create(self, vals):
        if vals.get('incident_id', _('New')) == _('New'):
            vals['incident_id'] = self.env['ir.sequence'].next_by_code('Safety_Incident_ID') or _('New')
        result = super(cwl_safety_incident, self).create(vals)
        return result

    @api.multi
    def back_to_web(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': '/employee/portal/'
        }




#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100