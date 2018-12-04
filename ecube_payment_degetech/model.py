# -*- coding: utf-8 -*-

from openerp import models, fields, api
from datetime import datetime, timedelta , date

class EcubeInvoiceExtenstionPayment(models.Model):
    _inherit = 'account.invoice'

    debit_account = fields.Many2one('account.move',string="Debit Account",track_visibility='onchange')
    journal_entry_id = fields.Many2one('account.move',string="Payment Link",readonly=True ,track_visibility='onchange')
    debit_account_id = fields.Many2one('account.account',string="Debit Account",track_visibility='onchange')
    payment_amount = fields.Float(string="Payment Amount",track_visibility='onchange')
    payment_done = fields.Boolean(string="Payment Done",track_visibility='onchange')



    @api.multi
    def payment_digitech(self):
        journal_entries = self.env['account.move']
        journal_entries_lines = self.env['account.move.line']
        if self.journal_entry_id:
            self.journal_entry_id.unlink()
        if not self.journal_entry_id:   
            create_journal_entry = journal_entries.create({
                    'journal_id': self.journal_id.id,
                    'date':date.today(),
                    'ref' : self.number,                     
                    })
            self.journal_entry_id = create_journal_entry.id
            create_debit = self.create_entry_lines(self.debit_account_id.id,self.payment_amount,0,create_journal_entry.id)
            create_credit = self.create_entry_lines(self.account_id.id,0,self.payment_amount,create_journal_entry.id)  


    def create_entry_lines(self,account,debit,credit,entry_id):
        self.env['account.move.line'].create({
                'account_id':account,
                'partner_id':self.partner_id.id,
                'name':self.reference or self.partner_id.name,
                'debit':debit,
                'credit':credit,
                'move_id':entry_id,
                })