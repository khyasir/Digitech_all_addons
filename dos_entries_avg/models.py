# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _
import math
class dos_journal_avg_entries(models.Model):
	_inherit = 'account.analytic.line'
	entries_hour_avg = fields.Float(compute="_compute_entries_hour_avg",string='Entries/Hour', store=True)
	hourly_avg_f = fields.Float(compute="_compute_hourly_avg_f", string='Hourly Avg', store=True )
	total_entries_hour_avg = fields.Float(compute="_compute_avg_cal_ent", string='Project Entries/Hour' ,store=True)
	total_hourly_avg_f = fields.Float(compute="_compute_avg_cal_ent", string='Project Hourly Avg',store=True)



	@api.depends('total_no_of_entries','total_no_of_hours')
	def _compute_entries_hour_avg(self):
		for rec in self:
			if rec.total_no_of_entries and rec.total_no_of_hours:
				avg_entries = rec.total_no_of_entries / rec.total_no_of_hours
				rec.entries_hour_avg =  avg_entries

	@api.depends('total_no_of_hours','amount')
	def _compute_hourly_avg_f(self):
		for rec in self:	
			if rec.total_no_of_hours and rec.amount:
				avg_hour = rec.amount / rec.total_no_of_hours
				rec.hourly_avg_f =  avg_hour



	@api.depends('total_no_of_entries', 'total_no_of_hours','amount')
	def _compute_avg_cal_ent(self):
		all_current_records = self.env['account.analytic.line'].search([('account_id','=',self.account_id.id)])
		entries = 0
		hours = 0
		amount = 0
		for i in all_current_records:
			entries += i.total_no_of_entries
			hours += i.total_no_of_hours
			amount += i.amount
		if self.total_no_of_hours > 0 and self.total_no_of_entries > 0:
			self.total_entries_hour_avg = entries / hours
		if self.total_no_of_hours > 0 and self.amount > 0:
			self.total_hourly_avg_f = amount / hours
