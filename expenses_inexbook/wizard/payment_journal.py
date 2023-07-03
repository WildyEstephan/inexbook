from odoo import api, fields, models


class PaymentJournal(models.TransientModel):
    _name = 'inex.payment.journal.wizard'
    _description = 'Payment Journal INEXBOOK Wizard'

    expense_id = fields.Many2one(
        comodel_name='inex.expense.request',
        string='Expense',
        required=False)
    journal_id = fields.Many2one(
        comodel_name='account.journal',
        string='Journal',
        required=False, domain=[('type', 'in', ('bank', 'cash'))])

    def create_payment(self):

        if self.expense_id.request_type=='advance_invoice':
            ID = self.env['account.payment'].create({
                'payment_type': 'outbound',
                'partner_id': self.expense_id.partner_id.id,
                'amount': self.expense_id.amount_total,
                'currency_id': self.expense_id.currency_id.id,
                'journal_id': self.journal_id.id,
                'ref': 'Pago ' + self.expense_id.name,
                'inex_expense_id': self.expense_id.id,
                'partner_type': 'supplier'
            })

            action = self.env['ir.actions.act_window']._for_xml_id('account.action_account_payments_payable')

            form_view = [(self.env.ref('account.view_account_payment_form').id, 'form')]

            action['views'] = form_view
            action['res_id'] = ID.id

        return action