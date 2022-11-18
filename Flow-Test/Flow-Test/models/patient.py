# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PatientDetails(models.Model):
    _name = 'patient.details'

    name = fields.Char(string="name", required=True)
    Emeregencyname = fields.Char(string="Name", required=True)
    p_id = fields.Many2one('patient.details', string="patient",required=True)
    relation = fields.Char(required=True, tracking=True)
    kebele = fields.Char(string="Kebele")
    House_No = fields.Char(string="House_No")
    Emeregencykebele = fields.Char(string="Kebele")
    EmeregencyHouse_No = fields.Char(string="House_No")
    patient_image = fields.Binary(string='Image', attachment=True)
    phone = fields.Char(string="Phone No", required=True)
    Emeregencyphone = fields.Char(string="Mobile", required=True)
    Home_Tel = fields.Char(string="Home_Tel", required=True)
    EmeregencyHome_Tel = fields.Char(string="Home_Tel", required=True)
    email = fields.Char(string="Email", required=True)
    Emeregencyemail = fields.Char(string="Email", required=True)
    age = fields.Integer(string='age', tracking=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'), 
        ], required=True, default='male', tracking=True)
    pid = fields.Many2one('res.partner' )
    city = fields.Char(string = "Sub_city")
    Emeregencycity = fields.Char(string="Sub_city")   
    @api.model
    def create(self, vals):
        sale = self.env['res.partner' ]
        val = {
            'name': vals['name']          
        }
        partner=sale.create(val)
        vals['pid'] = partner.id
        return super(PatientDetails, self).create(vals)
    def action_view_appointment_id_new(self):
	    return{
			'default_patient_id': self.p_id.id
		    }