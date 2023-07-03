from odoo import api, fields, models


class Invoice(models.Model):
    _inherit = 'account.move'

    inex_expense_id = fields.Many2one(
        comodel_name='inex.expense.request',
        string='Expense',
        required=False)
