# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
#from datetime import datetime, date
from datetime import datetime, timedelta

class m_a(models.Model):
	_name = "m.a"
	_inherit = 'mail.thread'

	name = fields.Char(string="Appointment ID", readonly=True ,copy=True)
	partner_id = fields.Many2one('res.partner',string="Health Center")
	p_id = fields.Many2one('patient.details',string="patient",required=True)
	appointment_date = fields.Datetime('Appointment Date',required=True,default = fields.Datetime.now)
	appointment_end = fields.Datetime('Appointment End',required=True)
	appointment_validity_date = fields.Datetime('Validity Date')
	comments = fields.Text(string="Info")
	# state = fields.Selection([('draft','Draft'),('confirmed','Confirm'),('cancel','Cancel'),('done','Done')],string="State",default='draft')	
	duration = fields.Integer('Duration')
	@api.model
	def create(self, vals):
		vals['name'] = self.env['ir.sequence'].next_by_code('m.a') or 'APT'
		msg_body = 'Appointment created'
		for msg in self:
			msg.message_post(body=msg_body)
		result = super(m_a, self).create(vals)
		return result
	def Appointment(self):
		print("jfndjbnjfeefd")

    # @api.model
    # def create(self, vals):
    #     event = super(CalendarEvent, self).create(vals)

    #     if event.vehicle_service_id and not event.activity_ids:
    #         event.vehicle_service_id.log_meeting(
    #             event.name, event.start, event.duration
    #         )
    #     return event
	
	
	# def confirm(self):
	# 	self.write({'state': 'confirmed'})

	# def done(self):
	# 	self.write({'state': 'done'})

	# def cancel(self):
	# 	self.write({'state': 'cancel'})
