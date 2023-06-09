from odoo import api, fields, models


class DocumentExpense(models.Model):
    _name = 'inex.document.expense'
    _description = 'Document Expense'

    name = fields.Char(
        string='Name',
        required=False)
    file_document = fields.Binary(string="Document",  )
    expense_id = fields.Many2one(
        comodel_name='inex.expense.request',
        string='Expense',
        required=False)

