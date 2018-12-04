# -*- coding: utf-8 -*-
from openerp import models, fields, api
class timesheet_create_custom_dos(models.Model):
	_inherit = 'hr.analytic.timesheet'
	task_mat_ts_id = fields.Integer('Timesheet id')
	fixed_entries = fields.Boolean('Fixed Check Box')

class timesheet_create_dos(models.Model):
	_inherit='project.task.materials'
	# for create timesheet entries of each line in project.task.materials
	@api.model
	def create(self, values):
		result =  super(timesheet_create_dos, self).create(values)
		product = values['product_id']
		journal = self.env.ref(
			'project_task_materials_stock.analytic_journal_sale_materials')
		#res = self.env['project.task.materials'].browse(values['task_id'])
		task_obj = self.env['project.task']
		task_obj = task_obj.browse(values['task_id'])
		negative_amount = values['amount_recalculate']
		negative_amount = negative_amount * -1
		analytic_account = getattr(values['task_id'], 'analytic_account_id', False)\
		or task_obj.project_id.analytic_account_id
		valuessss ={
				'date': values['date'],
				'name': values['description'],
				'user_id': values['done_by'],
				'product_id': product,
				'amount': negative_amount,
				'unit_amount': values['hours'],
				'account_id': analytic_account.id,
				'journal_id': journal.id,
				'task_mat_ts_id' : values['task_id'],
				'task_assigned_name' : task_obj.id,
				'task_name_hourly' : task_obj.id,
				'fixed_entries' : True,
				'task_fixed_entries' : values['quantity'],
				'total_no_of_entries' : values['quantity'],
				
				}
		timesheet_obj = self.env['hr.analytic.timesheet']
		timesheet_obj.create(valuessss)
		return result

class timesheet_prj_task_create_dos(models.Model):
	_inherit='project.task'
# for updating record in project_task_materials model and update entries in timesheet to
	@api.multi
	def write(self, values):
		res = super(timesheet_prj_task_create_dos, self).write(values)
		timeshee_recs = self.env['hr.analytic.timesheet'].search([('task_mat_ts_id','=',self.id)])
		timeshee_recs.unlink()
		for line in self.material_ids:
			product = line.product_id
			journal = self.env.ref(
				'project_task_materials_stock.analytic_journal_sale_materials')
			analytic_account = getattr(line.task_id, 'analytic_account_id', False)\
			or line.task_id.project_id.analytic_account_id
			# negative_amount = values['amount_recalculate']
			negative_amount = line.amount_recalculate * -1
			timesheet_obj = self.env['hr.analytic.timesheet']
			valuessss={
					'date': line.date,
					'name': line.description,
					'user_id': line.done_by.id,
					'product_id': product.id,
					'unit_amount': line.hours,
					'amount': negative_amount,
					'account_id': analytic_account.id,
					'task_assigned_name' : line.task_id.id,
					'task_name_hourly' : line.task_id.id,
					'journal_id': journal.id,
					'task_mat_ts_id' : line.task_id.id,
					'fixed_entries' : True,
					'task_fixed_entries' : line.quantity,
					'total_no_of_entries' : line.quantity,
					
					
				}
			timesheet_obj.create(valuessss)
		return res
# for deleting all entries of timesheet if task is deleted
	@api.multi
	def unlink(self):
		timeshee_recs = self.env['hr.analytic.timesheet'].search([('task_mat_ts_id','=',self.id)])
		timeshee_recs.unlink()
		return super(timesheet_prj_task_create_dos,self).unlink()
