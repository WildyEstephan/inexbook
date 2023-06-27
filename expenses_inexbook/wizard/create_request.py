from odoo import api, fields, models, _

class CreateRequest(models.TransientModel):
    _name = 'create.inex.request.wizard'
    _description = 'Create Request INEXBOOK Wizard'

    request_type = fields.Selection(
        string='Request Type',
        selection=[('advance_invoice', 'Advance Without Invoice'),
                   ('pay_invoice_without_po', 'Payment With Invoice Without Purchase Order'),
                   ('pay_to_supplier_with_po', 'Payment To Supplier With Purchase Order'),
                   ('refund', 'Refund With Invoice'),
                   ('credit_card_payment', 'Credit Card Payment'),
                   ('replacement_of_petty_cash', 'Replacement Of Petty Cash'),
                   ],
        required=False)

    def create_request(self):


        ID = self.env['inex.expense.request'].create({
            'request_type': self.request_type,
            'user_id': self.env.user.id
        })

        action = self.env['ir.actions.act_window']._for_xml_id('expenses_inexbook.inex_expense_request_action')

        form_view = [(self.env.ref('expenses_inexbook.inex_expense_request_view_form').id, 'form')]

        action['views'] = form_view
        action['res_id'] = ID.id

        return action
