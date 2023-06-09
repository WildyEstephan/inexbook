# -*- coding: utf-8 -*-
# from odoo import http


# class ExpensesInexbook(http.Controller):
#     @http.route('/expenses_inexbook/expenses_inexbook', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/expenses_inexbook/expenses_inexbook/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('expenses_inexbook.listing', {
#             'root': '/expenses_inexbook/expenses_inexbook',
#             'objects': http.request.env['expenses_inexbook.expenses_inexbook'].search([]),
#         })

#     @http.route('/expenses_inexbook/expenses_inexbook/objects/<model("expenses_inexbook.expenses_inexbook"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('expenses_inexbook.object', {
#             'object': obj
#         })
