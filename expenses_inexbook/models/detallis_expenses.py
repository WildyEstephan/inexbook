from odoo import api, fields, models, _

class DetallisExpenses(models.Model):
    _name = 'inex.expense.detail'
    _description = 'Detallis Expenses'

    name = fields.Char(
        string='Name',
        required=False)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Supplier',
        required=False)
    invoice_date = fields.Date(
        string='Invoice Date',
        required=False)
    no_invoice = fields.Char(
        string='No. Invoice',
        required=False)
    voucher_type = fields.Many2one(
        comodel_name='l10n_latam.document.type',
        string='Voucher Type',
        required=False)
    no_refund_note = fields.Text(
        string="No. Refund Note",
        required=False)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=False)
    category_id = fields.Many2one(
        comodel_name='product.category',
        string='Category',
        required=False)
    amount_untaxed = fields.Float(
        string='Amount Untaxed',
        required=False)
    taxes = fields.Many2many(
        comodel_name='account.tax',
        string='Taxes')
    amount_to_pay = fields.Float(
        string='Amount to pay',
        required=False)
    tips_cash = fields.Char(
        string='Tips Cash',
        required=False)
    expense_type = fields.Selection(
        string='Expense Type',
        selection=[
            ("01", _("01 - Personal")),
            ("02", _("02 - Work, Supplies and Services")),
            ("03", _("03 - Leasing")),
            ("04", _("04 - Fixed Assets")),
            ("05", _("05 - Representation")),
            ("06", _("06 - Admitted Deductions")),
            ("07", _("07 - Financial Expenses")),
            ("08", _("08 - Extraordinary Expenses")),
            ("09", _("09 - Cost & Expenses part of Sales")),
            ("10", _("10 - Assets Acquisitions")),
            ("11", _("11 - Insurance Expenses")),
        ],
        required=False, )
    filename_document = fields.Char(
        string='Filename Document',
        required=False)
    file_document = fields.Binary(string="Document",  )
    bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Bank Account',
        required=False, domain="[('partner_id', '=', partner_id)]")
    transfer_data = fields.Char(
        string='Transfer Data',
        required=False)
    summay_invoice = fields.Text(
        string="Summay Invoice",
        required=False)
    payment_way = fields.Selection(
        string='Payment Way',
        selection=[('cash', 'Cash'),
                   ('transaction', 'Transaction'),
                   ('card', 'Credit Card'),
                   ],
        required=False, )
    expense_id = fields.Many2one(
        comodel_name='inex.expense.request',
        string='Expense',
        required=False)


