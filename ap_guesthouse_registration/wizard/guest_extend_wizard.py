# -*- coding: utf-8 -*-
from odoo import fields, api, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date



class HotelGuestExtend(models.TransientModel):
    _name = 'guest.extend.wizard'
    _description = 'Guest Extend'

    @api.model
    def default_get(self, fields):
        res = super(HotelGuestExtend, self).default_get(fields)
        if (self.env.context.get('active_id')):
            regId = self.env.context.get('active_id')

            result = self.env['hotel.register'].browse(regId)

            res['guest_id'] = regId
            res['name'] = result.name
            res['booking_ref'] = result.booking_ref
            res['name'] = result.name
            res['arr_date'] = result.arr_date
            res['dep_date'] = result.dep_date
            res['booking_id'] = result.booking_id

            return res

    guest_id = fields.Integer('Id')
    booking_id = fields.Integer('Booking Id')
    name = fields.Char('Name')
    booking_ref = fields.Char('Booking Ref')
    arr_date = fields.Datetime(string='Arrival Date')
    dep_date = fields.Datetime(string='Departure Date')
    new_dep_date = fields.Datetime(string='New Departure Date')

    def action_extend_guest(self):
        print("guest extend clicked", self.new_dep_date, self.booking_id)
        dep_dt = self.dep_date
        n_date = self.new_dep_date
        bk_id = self.booking_id
        reg_id = self.guest_id
        new_dep_date = n_date.date().strftime("%Y-%m-%d") + " 06:00"

        if (n_date > dep_dt):

            vals1 = {
                'check_out_date': new_dep_date,
            }
            vals2 = {
                'dep_date': new_dep_date,
            }
            self.env['sale.order'].browse(bk_id).write(vals1)
            self.env['hotel.register'].browse(reg_id).write(vals2)

        else:
            raise ValidationError(
                _('Extend date must be grater than departure date!!!'))






