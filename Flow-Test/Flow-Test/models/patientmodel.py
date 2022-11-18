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
    start_visit = fields.Datetime(string="Start Visit", help='Visit check in time automatically'
                                                                 ' fills when he checked in to the hospital.')
    done = fields.Datetime(string="Finished Visit", help='Visit check out time automatically '
                                                                   'fills when he checked out from the hospital.')
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
    def action_cancel(self):
        self.state = "cancel"
    def action_start_visit(self):
        self.state = "start_visit"
        self.start_visit = datetime.datetime.now()
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
 
    
    class VisitPurpose(models.Model):
        _name = 'fo.purpose'
        name = fields.Char(string='Purpose', required=True, help='visit purpose in short term.eg:visit.')
        description = fields.Text(string='Description Of Purpose', help='Description for the Purpose.')