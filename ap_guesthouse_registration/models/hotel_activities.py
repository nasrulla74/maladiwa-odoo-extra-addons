# -*- coding: utf-8 -*-
from odoo import api, fields, models, _



class HotelExActivities(models.Model):
    _name = 'hotel.ex.activities'
    _description = 'Hotel Activities'

    name = fields.Char('Name', required=True)
    guest_id = fields.Many2one('hotel.register', required=True, string="Room No/Name", domain="[('reg_state', 'in', ['checked-in'])]")
    # guest_id = fields.Many2one('hotel.register', string="Room No/Name")
    provider_id = fields.Many2one('res.partner', string="Provider")
    ac_type = fields.Selection([('excursion', 'Excursion'), ('dinner', 'Dinner')],
                                 default='excursion', string="Type")
    ac_state = fields.Selection([('draft', 'Draft'), ('done', 'Done'), ('billed', 'Billed')],
                                 default='draft', string="State")
    ac_date = fields.Date(string='Activity Date', required=True, default=lambda self: fields.Datetime.now())
    remarks = fields.Char('Remarks')

    @api.onchange('guest_id')
    def onchange_guest_id(self):
        if(self.guest_id):
            self.name = self.guest_id.name



class HotelComplains(models.Model):
    _name = 'hotel.complain'
    _description = 'Guest Complains'

    name = fields.Char('Name', required=True)
    guest_id = fields.Many2one('hotel.register', required=True, string="Room No/Name", domain="[('reg_state', 'in', ['checked-in'])]")
    c_state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
                                 default='draft', string="State")
    c_date = fields.Datetime(string='Activity Date', required=True, default=lambda self: fields.Datetime.now())
    complete_at = fields.Datetime(string='Completed At')
    complain = fields.Text('Complaint/Request')

    @api.onchange('guest_id')
    def onchange_guest_id(self):
        if (self.guest_id):
            self.name = self.guest_id.name