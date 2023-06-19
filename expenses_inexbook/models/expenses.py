from odoo import api, fields, models, _


class ExpensesRequest(models.Model):
    _name = 'inex.expense.request'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = 'Expenses Request'

    name = fields.Char(
        string='Name',
        required=False)
    request_date = fields.Date(
        string='Request Date',
        required=False, default=fields.Date.today(), tracking=True)
    request_type = fields.Selection(
        string='Request Type',
        selection=[('advance_invoice', 'Advance Without Invoice'),
                   ('pay_invoice_without_po', 'Payment With Invoice Without Purchase Order'),
                   ('pay_to_supplier_with_po', 'Payment To Supplier With Purchase Order'),
                   ('refund', 'Refund With Invoice'),
                   ('credit_card_payment', 'Credit Card Payment'),
                   ('replacement_of_petty_cash', 'Replacement Of Petty Cash'),
                   ],
        required=True, tracking=True)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Requester',
        required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Beneficiary',
        required=False)
    beneficiary_type = fields.Selection(
        string='Beneficiary_type',
        selection=[('employee', 'Employee'),
                   ('supplier', 'Supplier'),
                   ],
        required=False, )
    subject = fields.Char(
        string="Subject",
        required=False, tracking=True)
    description = fields.Text(
        string="Description",
        required=False)
    amount_total = fields.Monetary(
        string='Amount Total',
        required=False)
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        required=False)
    state = fields.Selection(
        string='State',
        selection=[('request', 'Request'),
                   ('sent', 'Sent'),
                   ('department_approval', 'In Department Approval'),
                   ('business_leader_approval', 'In Business Leader Approval'),
                   ('accounting_record', 'In Accounting Record'),
                   ('finance_approval', 'In Finance Approval'),
                   ('president_approval', 'In President Approval'),
                   ('payment_process', 'In Payment Process'),
                   ('stopped', 'Stopped'),
                   ('paid', 'Paid'),
                   ('cancelled', 'Cancelled'),
                   ('request_correction', 'Request for Corrections'),
                   ],
        required=False, default='request', tracking=True)
    deadline_payment = fields.Date(
        string='Deadline Payment',
        required=False)
    project_account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Project',
        required=False)
    payment_way = fields.Selection(
        string='Payment Way',
        selection=[('cash', 'Cash'),
                   ('transaction', 'Transaction'),
                   ('card', 'Credit Card'),
                   ],
        required=False, )
    time_readjustment = fields.Many2one(
        comodel_name='inex.time.readjustment',
        string='Time Readjustment',
        required=False)

    # PAYMENT WITH INVOICE WITHOUT PURCHASE ORDER
    invoice_date = fields.Date(
        string='Invoice Date',
        required=False)
    no_invoice = fields.Char(
        string='No. Invoice',
        required=False)
    # invoice_id = fields.Many2one(
    #     comodel_name='account.move',
    #     string='No. Invoice',
    #     required=False, domain="[('move_type', '=', 'in_invoice')]")
    voucher_type = fields.Many2one(
        comodel_name='l10n_latam.document.type',
        string='Voucher Type',
        required=False)
    number_voucher = fields.Char(
        string='Number Voucher',
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
    document_ids = fields.One2many(
        comodel_name='inex.document.expense',
        inverse_name='expense_id',
        string='Documents',
        required=False)
    bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Bank Account',
        required=False, domain="[('partner_id', '=', partner_id)]")
    transfer_data = fields.Text(
        string='Transfer Data',
        required=False)
    summary_invoice = fields.Text(
        string="Summary Invoice",
        required=False)

    # PAYMENT TO SUPPLIER WITH PURCHASE ORDER
    purchase_id = fields.Many2one(
        comodel_name='purchase.order',
        string='Purchase',
        required=False)
    detail_ids = fields.One2many(
        comodel_name='inex.expense.detail',
        inverse_name='expense_id',
        string='Details',
        required=False)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'expense.inex.request') or _('New')
        res = super(ExpensesRequest, self).create(vals)
        return res

    def sent(self):
        self.state = 'sent'

    def approve_inexbook_manager(self):
        self.state = 'department_approval'

    def approve_inexbook_business_leader(self):
        self.state = 'business_leader_approval'

    def approve_accounting(self):
        self.state = 'accounting_record'

    def approve_CFO(self):
        self.state = 'finance_approval'

    def approve_CEO(self):
        self.state = 'president_approval'

    def pay_this(self):
        self.state = 'payment_process'

    def stop_this(self):
        self.state = 'stopped'

    def cancel_this(self):
        self.state = 'cancelled'

    def request_corrections(self):
        self.state = 'request_correction'









