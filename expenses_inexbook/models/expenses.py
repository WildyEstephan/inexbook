from odoo import api, fields, models, Command, _
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError
from odoo.tools import float_compare, float_is_zero, date_utils, email_split, email_re, html_escape, is_html_empty
from odoo.tools.misc import formatLang, format_date, get_lang
from odoo.osv import expression

from datetime import date, timedelta
from collections import defaultdict
from contextlib import contextmanager
from itertools import zip_longest
from hashlib import sha256
from json import dumps

import ast
import json
import re
import warnings

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
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=False, default=lambda self: self.env.user.company_id.id)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Requester',
        required=True)
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Beneficiary',
        required=False)
    beneficiary_type = fields.Selection(
        string='Beneficiary Type',
        selection=[('employee', 'Employee'),
                   ('supplier', 'Supplier'),
                   ],
        required=False, compute='_compute_beneficiary_type')
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
        required=False, default=lambda self: self.env.user.company_id.currency_id.id)
    state = fields.Selection(
        string='State',
        selection=[('request', 'Request'),
                   ('sent', 'Sent'),
                   ('department_approval', 'In Department Approval'),
                   ('business_leader_approval', 'In Business Leader Approval'),
                   ('accounting_record', 'In Accounting Record'),
                   # ('finance_approval', 'In Finance Approval'),
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
    voucher_type = fields.Many2one(
        comodel_name='l10n_latam.document.type',
        string='Voucher Type',
        required=False)
    number_voucher = fields.Char(
        string='Number Voucher',
        required=False)
    no_refund_note = fields.Text(
        string="No. Refund Note",
        required=False, compute='_compute_no_refund_note')
    no_refund_note_html = fields.Html(
        string='Refund Notes',
        required=False, compute='_compute_no_refund_note')
    amount_on_credit = fields.Float(
        string='Amount on Credit',
        required=False, compute='_compute_no_refund_note')
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=False)
    category_id = fields.Many2one(
        comodel_name='product.category',
        string='Category',
        required=False)
    amount_untaxed = fields.Monetary(
        string='Amount Untaxed',
        required=False)
    taxes = fields.Many2many(
        comodel_name='account.tax',
        string='Taxes')
    amount_to_pay = fields.Float(
        string='Amount to pay',
        required=False, compute='_compute_amount_to_pay')
    amount_to_pay_net = fields.Float(
        string='Amount to Pay to Supplier',
        required=False, compute='_compute_amount_to_pay_net')
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
    count_document = fields.Integer(
        string='Count Documents',
        required=False, compute='_compute_count_document')
    attached_document = fields.Binary(string="Attached Document", )
    filename_attached_document = fields.Char(
        string='Filename attached document',
        required=False)
    bank_id = fields.Many2one(
        comodel_name='res.partner.bank',
        string='Bank Account',
        required=False, domain="[('partner_id', '=', partner_id)]")
    transfer_data = fields.Text(
        string='Transfer Data',
        required=False)
    tax_totals_json = fields.Text(
        string="Summary Invoice",
        required=False, compute='_compute_tax_totals_json')

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

    # PAYMENT TO CREDIT CARD
    credit_card_id = fields.Many2one(
        comodel_name='inex.credit.card',
        string='Credit Card',
        required=False)

    @api.depends('number_voucher')
    def _compute_no_refund_note(self):

        # no_refund_note_html
        # amount_on_credit

        for rec in self:
            if rec.number_voucher:
                credit_note = self.env['account.move'].search([('l10n_do_origin_ncf', '=', rec.number_voucher)])

                list_refund_note = ""
                list_refund_note_hmtl = ""
                total = 0.0
                for note in credit_note:
                    total += note.amount_total_in_currency_signed
                    list_refund_note += note.l10n_do_fiscal_number + ' ' + fields.Date.to_string(note.invoice_date) + ' ' + \
                                        note.currency_id.symbol + ' ' + str(note.amount_total_in_currency_signed) + '\n'
                    list_refund_note_hmtl += note.l10n_do_fiscal_number + ' ' + fields.Date.to_string(note.invoice_date) + ' ' + \
                                        note.currency_id.symbol + ' ' + str(note.amount_total_in_currency_signed) + '<br/>'

                rec.no_refund_note = list_refund_note

                rec.no_refund_note_html = "<p style='color:blue;'>" + list_refund_note_hmtl + "</p>"
                rec.amount_on_credit = total
            else:
                rec.no_refund_note = ""

                rec.no_refund_note_html = ""
                rec.amount_on_credit = 0

    @api.depends('amount_untaxed', 'taxes')
    def _compute_amount_to_pay(self):
        for rec in self:
            taxes = rec.taxes.compute_all(rec.amount_untaxed, rec.currency_id, 1,
                                            product=rec.product_id, partner=rec.partner_id)
            rec.amount_to_pay = taxes['total_included']

    @api.depends('amount_on_credit', 'amount_to_pay')
    def _compute_amount_to_pay_net(self):

        for rec in self:
            rec.amount_to_pay_net = rec.amount_to_pay - rec.amount_on_credit


    @api.depends('document_ids')
    def _compute_count_document(self):
        for rec in self:
            rec.count_document = len(rec.document_ids)

    def action_view_document(self):
        documents = self.mapped('document_ids')
        action = self.env["ir.actions.actions"]._for_xml_id("expenses_inexbook.inex_document_expense_action")
        if len(documents) > 1:
            action['domain'] = [('id', 'in', documents.ids)]
        elif len(documents) == 1:
            action['domain'] = [('id', '=', documents.id)]
        else:
            action = {'type': 'ir.actions.act_window_close'}

        context = {
                'default_expense_id': self.id,
            }
        action['context'] = context

        return action


    @api.depends('partner_id')
    def _compute_beneficiary_type(self):

        for rec in self:

            if rec.partner_id.employee_ids:
                rec.beneficiary_type = 'employee'
            else:
                rec.beneficiary_type = 'supplier'


    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'expense.inex.request') or _('New')
        res = super(ExpensesRequest, self).create(vals)
        return res

    def send_this(self):
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

    def payment_process_this(self):
        self.state = 'payment_process'

    def pay_this(self):
        self.state = 'paid'

    def stop_this(self):
        self.state = 'stopped'

    def cancel_this(self):
        self.state = 'cancelled'

    def request_corrections(self):
        self.state = 'request_correction'

    def _get_expense_account_source(self):
        self.ensure_one()
        if self.account_id:
            account = self.account_id
        elif self.product_id:
            account = self.product_id.product_tmpl_id.with_company(self.company_id)._get_product_accounts()['expense']
            if not account:
                raise UserError(
                    _("No Expense account found for the product %s (or for its category), please configure one.") % (
                        self.product_id.name))
        else:
            account = self.env['ir.property'].with_company(self.company_id)._get('property_account_expense_categ_id',
                                                                                 'product.category')
            if not account:
                raise UserError(
                    _('Please configure Default Expense account for Category expense: `property_account_expense_categ_id`.'))
        return account

    @api.depends('partner_id', 'currency_id', 'amount_untaxed', 'amount_to_pay', 'taxes')
    def _compute_tax_totals_json(self):
        """ Computed field used for custom widget's rendering.
            Only set on invoices.
        """
        for rec in self:
            rec.tax_totals_json = json.dumps({
                **rec._get_tax_totals(rec.amount_untaxed, rec.currency_id, rec.product_id,
                                      rec.partner_id, rec.taxes, rec.amount_to_pay),
            })

    @api.model
    def _get_tax_totals(self, amount_untaxed, currency_id, product_id, partner_id, taxes_list, amount_to_pay):

        groups_by_subtotal = {}
        subtotals_list = []

        if taxes_list:
            account_tax = self.env['account.tax']

            taxes = taxes_list.compute_all(amount_untaxed, currency_id, 1,
                                          product=product_id, partner=partner_id)['taxes']

            group_ids = []

            for tax_g in taxes:
                cleaned_id = 0
                if 'New' in str(tax_g['id']):
                    cleaned_id =  int(str(tax_g['id'])[6:])
                else:
                    cleaned_id = tax_g['id']

                group_ids.append(account_tax.search([('id', '=', cleaned_id)], limit=1).tax_group_id.id)

            tax_grouped = {}

            for tax in taxes_list:
                if 'New' in str(tax['id']):
                    cleaned_id = int(str(tax['id'])[6:])
                else:
                    cleaned_id = tax['id']
                tax_id = account_tax.search([('id', '=', cleaned_id)], limit=1)

                if tax_id.tax_group_id.id in tax_grouped.keys():
                    total = tax_grouped[tax_id.tax_group_id.id]['tax_group_amount'] + amount_untaxed * (tax['amount']/100)
                    tax_grouped[tax_id.tax_group_id.id]['tax_group_amount'] = total
                    tax_grouped[tax_id.tax_group_id.id]['formatted_tax_group_amount'] = formatLang(self.env, total,
                                                                                                   currency_obj=currency_id)
                else:
                    tax_grouped[tax_id.tax_group_id.id] = {
                        'tax_group_name': tax_id.tax_group_id.name,
                        'tax_group_amount': amount_untaxed * (tax['amount']/100),
                        'tax_group_base_amount': amount_untaxed,
                        'formatted_tax_group_amount': formatLang(self.env, amount_untaxed * (tax['amount']/100), currency_obj=currency_id),
                        'formatted_tax_group_base_amount': formatLang(self.env, amount_untaxed,
                                                                      currency_obj=currency_id),
                        'tax_group_id': tax_id.tax_group_id.id,
                        'group_key': '%s-%s' % ("Base Imponible", tax_id.tax_group_id.id)
                    }

            # Compute groups_by_subtotal
            groups_by_subtotal = {"Base Imponible": []}

            for group_id in group_ids:
                groups_by_subtotal["Base Imponible"].append(tax_grouped[group_id])

            # Compute subtotals
            subtotals_list = [{
                    'name': "Base Imponible",
                    'amount': amount_untaxed,
                    'formatted_amount': formatLang(self.env, amount_untaxed, currency_obj=currency_id),
                }]  # List, so that we preserve their order

        # Assign json-formatted result to the field
        return {
            'amount_total': amount_to_pay,
            'amount_untaxed': amount_untaxed,
            'formatted_amount_total': formatLang(self.env, amount_to_pay, currency_obj=currency_id),
            'formatted_amount_untaxed': formatLang(self.env, amount_untaxed, currency_obj=currency_id),
            'groups_by_subtotal': groups_by_subtotal,
            'subtotals': subtotals_list,
            'allow_tax_edition': False,
        }










