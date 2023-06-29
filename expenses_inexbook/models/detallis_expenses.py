from odoo import api, fields, models, _

class DetallisExpenses(models.Model):
    _name = 'inex.expense.detail'
    _description = 'Detallis Expenses'

    name = fields.Char(
        string='Description',
        required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Supplier',
        required=True)
    invoice_date = fields.Date(
        string='Invoice Date',
        required=True)
    no_invoice = fields.Char(
        string='No. Invoice',
        required=True)
    voucher_type = fields.Many2one(
        comodel_name='l10n_latam.document.type',
        string='Voucher Type',
        required=True)
    no_refund_note = fields.Text(
        string="No. Refund Note",
        required=False)
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True)
    category_id = fields.Many2one(
        comodel_name='product.category',
        string='Category',
        required=True)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        required=False, related='expense_id.currency_id')
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
    file_document = fields.Binary(string="Document",  required=True)
    bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Bank Account',
        required=True, domain="[('partner_id', '=', partner_id)]")
    transfer_data = fields.Char(
        string='Transfer Data',
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


