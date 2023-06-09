from odoo import api, fields, models


class TimeReadjustment(models.Model):
    _name = 'inex.time.readjustment'
    _description = 'Time Readjustment'

    name = fields.Char(
        string='Name',
        required=True)
    count_days = fields.Integer(
        string='Days',
        required=False)

