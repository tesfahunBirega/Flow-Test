# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PatientDetails(models.Model):
    _name = 'patient.details'

    name = fields.Char(string="name", required=True)
    Ename = fields.Char(string="Name", required=True)
    relation = fields.Selection([
        ('family', 'Family'),
        ('friend', 'Friend'),
        ('other', 'Other'), 
        ], required=True, default='family', tracking=True)
    street = fields.Char(string="Street")
    street2 = fields.Char(string="Street2")
    street3 = fields.Char(string="Street")
    street4 = fields.Char(string="Street2")
    patient_image = fields.Binary(string='Image', attachment=True)
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    phone = fields.Char(string="Phone No", required=True)
    Ephone = fields.Char(string="Mobile", required=True)
    Home_Tel = fields.Char(string="Home_Tel", required=True)
    EHome_Tel = fields.Char(string="Home_Tel", required=True)
    # Relation = fieds.Char(string="Relation", required=True)
    email = fields.Char(string="Email", required=True)
    Eemail = fields.Char(string="Email", required=True)
    age = fields.Integer(string='age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'), 
        ], required=True, default='male', tracking=True)
    pid = fields.Many2one('res.partner' )
    # company_info = fields.Many2one('res.partner', string="Company", help='Visiting persons company details')
    # zip = fields.Char(change_default=True)
    city = fields.Char()
    Ecity = fields.Char()
    # country_id = fields.Many2one('res.number', string='Country', ondelete='restrict')
    id_proof = fields.Many2one('id.proof', string="ID Proof")
    id_proof_no = fields.Char(string="Card No", help='Id proof number')
    visit_count = fields.Integer(compute='_no_visit_count', string='# Visits')
   
#    _sql_constraints = [
#         ('field_uniq_email_and_id_proof', 'unique (email,id_proof)', "Please give the correct data !"),
#     ]
# @api.multi
#     def _no_visit_count(self):
#         data = self.env['fo.visit'].search([('visitor', '=', self.ids), ('state', '!=', 'cancel')]).ids
#         self.visit_count = len(data)
    @api.model
    def create(self, vals):
        sale = self.env['res.partner' ]
        print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh',self.name)
        val = {
            'name': vals['name']          
        }
        partner=sale.create(val)
        vals['pid'] = partner.id
        return super(PatientDetails, self).create(vals)
    @api.model
    def create(self,valss):
        perchase = self.env['res.partner']
        vals = {
            'name': valss['name']
        }
        partner=perchase.create(vals)
        valss['pid'] = partner.id
        return super(PatientDetails, self).create(valss)

class VisitorProof(models.Model):
    _name = 'id.proof'
    _rec_name = 'id_proof'

    id_proof = fields.Char(string="Name")
    code = fields.Char(string="Code")