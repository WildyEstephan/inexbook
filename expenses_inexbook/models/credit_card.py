from odoo import api, fields, models, _ 


class CreditCard(models.Model):
    _name = 'inex.credit.card'
    _description = 'Credit Card'

    name = fields.Char(
        string='Number', 
        required=True)
    assigned_to = fields.Many2one(
        comodel_name='hr.employee',
        string='Assigned To',
        required=True)

    
