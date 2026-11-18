# -*- coding: utf-8 -*-

from odoo import fields, models, api

class AddPONumber(models.Model):
    _inherit = 'account.move'
    po_number = fields.Char('PO Number')

