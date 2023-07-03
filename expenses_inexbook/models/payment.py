from odoo import api, fields, models


class Payment(models.Model):
    _inherit = 'account.payment'

    inex_expense_id = fields.Many2one(
        comodel_name='inex.expense.request',
        string='Expense',
        required=False)
