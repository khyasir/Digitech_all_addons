# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools.translate import _
class account_move_line_custom_dos(models.Model):
	_inherit = 'account.move.line'
	difference_dr_cr = fields.Float(string='Balance')

	@api.onchange('debit','credit')
	def onchange_debit_credit_field(self):
		self.difference_dr_cr = self.debit - self.credit


	@api.model
	def create(self, values):
		values['difference_dr_cr'] = values['debit'] - values['credit']
		result = super(account_move_line_custom_dos, self).create(values)
		return result