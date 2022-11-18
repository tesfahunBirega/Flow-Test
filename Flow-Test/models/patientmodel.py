# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api, _

class PatientVisit(models.Model):
    _name = 'patient.visit'
    _inherit = ['mail.thread']
    _description = 'Visit'
    product_ids =fields.Many2many('product.product', string = 'servics')
    name = fields.Char(string="sequence", default=lambda self: _('New'))
    patient = fields.Many2one("patient.details", string='patient')
    phone = fields.Char(string="Phone", required=True)
    email = fields.Char(string="Email", required=True)
    reason = fields.Many2many('fo.purpose', string='Purpose Of Visit', required=True,
                              help='Enter the reason for visit')
    # product = fields.Many2one("product.product", string="Product")
    # parent_product = fields.Many2one("product.product", string="Product")
                   
    # visitor_belongings = fields.One2many('fo.belongings', 'belongings_id_fov_visitor', string="Personal Belongings",
    #                                      help='Add the belongings details here.')
    start_visit = fields.Datetime(string="Start Visit", help='Visit check in time automatically'
                                                                 ' fills when he checked in to the office.')
    done = fields.Datetime(string="Finished Visit", help='Visit check out time automatically '
                                                                   'fills when he checked out from the office.')
    visiting_doctor = fields.Many2one('hr.employee',  string="Visiting With")
    # patientUse = fields.Boolean(string='PatientUse', default=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('start_visit', 'Start Visit'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
     ], track_visibility='onchange', default='draft')


    @api.model
    def create(self, vals):
        if vals:
            vals['name'] = self.env['ir.sequence'].next_by_code('patient.visit') or _('New')
            result = super(PatientVisit, self).create(vals)
            return result
    # @api.model
    def action_cancel(self):
        self.state = "cancel"
    # @api.one
    def action_start_visit(self):
        self.state = "start_visit"
        self.start_visit = datetime.datetime.now()
    # @api.one
    def action_done(self):
        self.state = "done"
        self.done = datetime.datetime.now()  
        sale = self.env['sale.order' ]
        val = {
            'partner_id':self.patient.pid.id

        }
        sale_object=sale.create(val)
        sale_line = self.env['sale.order.line' ]
        for product in self.product_ids:
            val = {
                "product_id": product.id,
                "product_template_id":product.product_tmpl_id.id,
                "order_id": sale_object.id,
                'name': product.name,
                'price_unit': product.list_price,
                'product_uom_qty': 1,
                'customer_lead': 30,
                'company_id': sale_object.company_id.id,
            }
            order_line_object = self.env['sale.order.line'].create(val)
            sale_object.write({'order_line': [(4, order_line_object.id)]})
            
        purchase = self.env['purchase.order' ]
        vals = {
            'partner_id':self.patient.pid.id
        }
        purchase_object=purchase.create(vals)
        purchase_line = self.env['purchase.order.line']
        for product in self.product_ids:
            vals = {
                "product_id": product.id,
                "order_id": purchase_object.id,
                'name': product.name,
                'price_unit': product.list_price,
                'product_qty': 1,
                # 'customer_lead': 30,
                'company_id': purchase_object.company_id.id,
            }
        order_line_object = self.env['purchase.order.line'].create(vals)
        purchase_object.write({'order_line': [(4, order_line_object.id)]})
    @api.onchange('patient')
    def visitor_details(self):
        if self.patient:
            if self.patient.phone:
                self.phone = self.patient.phone
            if self.patient.email:
                self.email = self.patient.email
    # @api.onchange('visiting_doctor')
    # def get_employee_dpt(self):
    #     if self.visiting_doctor:
    #         self.department = self.visiting_doctor.department_id

    # class PersonalBelongings(models.Model):
    # _name = 'fo.belongings'

    # property_name = fields.Char(string="Property", help='Employee belongings name')
    # property_count = fields.Char(string="Count", help='Count of property')
    # number = fields.Integer(compute='get_number', store=True, string="Sl")
    # belongings_id_fov_visitor = fields.Many2one('fo.visit', string="Belongings")
    # belongings_id_fov_employee = fields.Many2one('fo.property.counter', string="Belongings")
    # permission = fields.Selection([
    #     ('0', 'Allowed'),
    #     ('1', 'Not Allowed'),
    #     ('2', 'Allowed With Permission'),
    #     ], 'Permission', required=True, index=True, default='0', track_visibility='onchange')
    
    class VisitPurpose(models.Model):
        _name = 'fo.purpose'
        name = fields.Char(string='Purpose', required=True, help='visit purpose in short term.eg:visit.')
        description = fields.Text(string='Description Of Purpose', help='Description for the Purpose.')