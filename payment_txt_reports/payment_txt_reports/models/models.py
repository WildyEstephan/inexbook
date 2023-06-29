# -*- coding: utf-8 -*-

import base64
from datetime import datetime as dt
from odoo import models, fields, api


class payment_txt_reports(models.Model):
    _inherit = 'account.payment'

    txt_binary = fields.Binary(string='txt file')
    txt_filename = fields.Char(string='txt filename')
    header_sequence = fields.Char(string="Header Sequence", store=True, compute="_compute_header_sequence")

    @api.depends('txt_binary')
    def _compute_header_sequence(self):

        for rec in self:
            n = self.header_sequence[-1]
            if rec.header_sequence == "":
                rec.header_sequence = "0000001"
            else:
                rec.header_sequence = "000000"+str(int(n) + 1)

    def download_txt(self):
        # STRUCTURE OF FILE
        # header of document
        constants = "EBO"
        spaces = ""
        rnc = self.company_id.vat

        # Condition for the spaces in rnc if it is less than 11
        if len(rnc) < 11:
            rncspaces = 11 - len(str(rnc))
            constants = constants + spaces.ljust(rncspaces)
        file_path = './{}'
        with open(file_path, 'w', encoding="utf-8", newline='\r\n') as txt:
            # for line in lines:
            txt.write("line" + '\n')

        self.write({

            'txt_binary': base64.b64encode(open(file_path, 'rb').read())

        })
        # NAME DOCUMENT
        name_document = "PE" + self.company_id.vat
        type_service = ['02',]
        period = dt.now().strftime("%m%d")

        # ext_document = ".txt"
        full_document = name_document + type_service[0] + period + self.header_sequence + "E"
        path = "/web/binary/download_document_tss?"
        model = "account.payment"
        filename = full_document

        url = path + "model={}&id={}&filename={}.txt".format(
            model, self.id, filename
        )
        return {

            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
            'tag': 'reload',
        }




