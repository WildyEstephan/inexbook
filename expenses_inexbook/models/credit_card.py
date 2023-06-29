from odoo import api, fields, models, _ 


class CreditCard(models.Model):
    _name = 'inex.credit.card'
    _description = 'Credit Card'

    name = fields.Char(
        string='Number', 
        required=True)
    bank_id = fields.Many2one(
        comodel_name='res.bank',
        string='Bank',
        required=False)
    assigned_to = fields.Many2one(
        comodel_name='hr.employee',
        string='Assigned To',
        required=True)

    
