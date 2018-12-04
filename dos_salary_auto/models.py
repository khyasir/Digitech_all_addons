# -*- coding: utf-8 -*-

from openerp import models, fields, api

class comput_amanat(models.Model):
	_inherit = 'hr.employee'
	@api.model
	def hourly_salary(self, payslip):
		duration = 0.0
		tsheet_obj = self.env['account.analytic.line']
		timesheets = tsheet_obj.search([('user_id.employee_ids', '=', payslip.employee_id),
				('date', '>=', payslip.date_from), ('date', '<=', payslip.date_to),('journal_id.code', '=', "TS")])
		for tsheet in timesheets:
			duration += tsheet.amount
		return duration * -1
		print duration

	@api.model
	def fixed_salary(self, payslip):
		duration = 0.0
		tsheet_obj = self.env['account.analytic.line']
		timesheets = tsheet_obj.search([('user_id.employee_ids', '=', payslip.employee_id),
				('date', '>=', payslip.date_from), ('date', '<=', payslip.date_to),('journal_id.code', '=', "SALMAT")])
		for tsheet in timesheets:
			duration += tsheet.amount
		return duration * -1
		print duration







