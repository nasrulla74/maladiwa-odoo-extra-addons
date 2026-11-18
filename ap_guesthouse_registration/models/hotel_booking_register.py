# -*- coding: utf-8 -*-
from email.policy import default
import string
from unicodedata import category
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class InheritPartner(models.Model):
    _inherit = 'res.partner'
    is_guest = fields.Boolean(string='Is Guest', default=False)
    x_is_checked_out = fields.Boolean(string='Is Checked Out', default=False)
    x_room_no = fields.Char('Room No')


    # def inhouse_guests(self):
    #     inhouse_guests = self.search([('is_guest', '=', 'True')])
    #     return inhouse_guests.ids



# class InheritMealPlan(models.Model):
#     _inherit = 'hotel.meal'

class HotelRegister(models.Model):
    _name = 'hotel.register'
    _description = 'Hotel Check-In / Register'

    guest_id = fields.Many2one('res.partner', 'Guest')

    name = fields.Char('Guest Name', required=True)
    booking_ref = fields.Char('Booking Ref')
    reg_no = fields.Char('Register No', required=True, copy=False, default=lambda self: _('New'))
    _rec_name = 'name'
    arr_date = fields.Datetime(string='Arrival Date', required=True)
    dep_date = fields.Datetime(string='Departure Date', required=True)
    bk_method = fields.Selection([('foreign-operator', 'Foreign tour operator'), ('local-operator', 'Local tour operator'), ('direct-fit', 'Direct booking/(FIT)'), ('ota', 'Online travel agent')],
                             default='ota', string="Booking Method")
    no_of_days = fields.Integer('No of Days', default=0)
    reg_category = fields.Selection([('guest', 'Guest'), ('maldivian', 'Maldivian'), ('expatriate', 'Expatriate')],
                             default='guest', string="Category",required=True)
    category_int = fields.Integer('Category', default=0)
    room_id = fields.Many2one('hotel.rooms',string="Room No")
    booking_id = fields.Many2one('sale.order', string="Booking")
    country_id = fields.Many2one('res.country', 'Country')
    meal_id = fields.Many2one('hotel.meal', string="Meal Plan")
    rm_cat_id = fields.Many2one('room.category', string="Room Category")
    identification_no = fields.Char('Identification No', required=True)
    #identification_no = fields.Char(related='guest_id.identification_no', string="Identification No")
    reg_state = fields.Selection([('checked-in', 'Checked-In'), ('checked-out', 'Checked-Out'), ('no_show', 'No Show')],
                             default='checked-in', string="Reg. Status")
    currency_id = fields.Many2one('res.currency', compute='_get_company_currency', readonly=True,
                                  string="Currency")  # currency of amount currency
    due_amount = fields.Monetary('Due Amount', compute='_customer_due_amount', default=0)
    date_of_birth = fields.Date("Date of Birth")

    def name_get(self):

        res = []
        for rec in self:
            name = rec.name
            if rec.room_id:
                name = rec.room_id.name + ' - ' + name
                res.append((rec.id, name))
            else:
                res.append((rec.id, name))

        return res


    # @api.model
    # def create(self, vals):
    #     if vals.get('reg_no', _('New')) == _('New'):
    #         vals['reg_no'] = self.env['ir.sequence'].next_by_code('guesthouse.register') or _('New')
    
    @api.onchange('reg_category')
    def onchange_reg_category(self):
        #for rec in self:
        country_obj = self.country_id 
        cid = country_obj.search([('name','=','Maldives')])

        if cid: 
            print("--------------------------------", cid.id) 
        if self.reg_category == 'guest':
            self.category_int = 1
        elif self.reg_category == "maldivian":
            self.category_int = 2
            if cid:
                self.country_id = cid
        elif self.reg_category == "expatriate":
            self.category_int = 3
        else:
            self.category_int = 1

    @api.onchange('country_id')
    def onchange_country_id(self):
        #for rec in self:
        country_obj = self.country_id 
        if country_obj.name == "Maldives":
            self.reg_category = "maldivian"

            print("--------------------------------", country_obj.name)


    def _customer_due_amount(self):
        self.due_amount = 0

        if not self.ids:
            return True

        print('pringting self', self.ids)

        domain = [
            ('partner_id', 'in', self.guest_id.ids),
            ('state', 'not in', ['draft', 'cancel']),
            ('move_type', 'in', ('out_invoice', 'out_refund')),
        ]


        price_totals = self.env['account.move'].read_group(domain, ['amount_residual_signed'], ['partner_id'])

        for bal in price_totals:
            print("Balance Due!", bal['partner_id'])
            print("Balance Due!", bal['amount_residual_signed'])
            for reg in self:
                if(reg.guest_id.id == bal['partner_id'][0]) :
                    print("yes")
                    reg.due_amount = bal['amount_residual_signed']




        # for reg in self:
        #     domain = [
        #         ('partner_id', 'in', reg.guest_id.ids),
        #         ('state', 'not in', ['draft', 'cancel']),
        #         ('move_type', 'in', ('out_invoice', 'out_refund')),
        #     ]
        #
        #
        #     price_totals = self.env['account.move'].read_group(domain, ['amount_residual_signed'], ['partner_id'])
        #
        #     print(price_totals)
        #     for bal in price_totals:
        #         print("balance due", bal['amount_residual_signed'])

                # self.due_amount = bal['amount_residual_signed']


        all_partners_and_children = {}
        # all_partner_ids = self['guest_id'].ids
        # all_reg_ids = self['id'].ids

        # for partner in self.filtered('guest_id'):
        #     # price_total is in the company currency
        #     all_partners_and_children[partner] = self.with_context(active_test=False).search([('guest_id', 'child_of', partner.id)]).ids
        #     all_partner_ids += all_partners_and_children[partner]

        # print('all_partners_and_children', all_partners_and_children)
        # print('all_partner_ids', all_partner_ids)

        # domain = [
        #     ('partner_id', 'in', all_partner_ids),
        #     ('state', 'not in', ['draft', 'cancel']),
        #     ('move_type', 'in', ('out_invoice', 'out_refund')),
        # ]
        # price_totals = self.env['account.invoice.report'].read_group(domain, ['price_subtotal'], ['partner_id'])
        # for partner, child_ids in all_partners_and_children.items():
        #     partner.due_amount = sum(price['price_subtotal'] for price in price_totals if price['partner_id'][0] in child_ids)
        # price_totals = self.env['account.invoice.report'].read_group(domain, ['price_subtotal'], ['partner_id'])
        # print((price_totals))
        # for reg in all_reg_ids:
        #     reg.due_amount = price_totals['price_subtotal']


    def _get_company_currency(self):
        for partner in self:
            if partner.guest_id.company_id:
                partner.currency_id = partner.guest_id.sudo().company_id.currency_id
            else:
                partner.currency_id = self.env.company.currency_id

    def write(self, vals):

        res = super(HotelRegister, self).write(vals)

        self.guest_id.is_guest = True
        if(self.room_id):
            self.guest_id.x_room_no = self.room_id.name
            self.guest_id.street = 'Room No: ' + self.room_id.name
            self.guest_id.phone = self.room_id.name
        # self.room_id.room_state = 'occupied'
        return res

    def action_check_out(self):
        print('checkout-action....', self)
        self.guest_id.x_is_checked_out = True
        self.booking_id.bk_state = 'check_out'
        # self.room_id.room_state = 'vacant'
        return self.write({'reg_state': 'checked-out'})


    def update_room_status(self):
        pass

    # def action_extend(self):
    #     print('extedn clcik')

    def action_test(self):
        print(self.guest_id.id)
        pos_balance_due = self.env['pos.order'].search([{'id','=',83}])



    def appeul_action_view_partner_invoices(self):
        self.ensure_one()
        print(self.guest_id.id)

        action = self.env["ir.actions.actions"]._for_xml_id("account.action_move_out_invoice_type")
        # all_child = self.with_context(active_test=False).search([('id', 'child_of', self.guest_id)])
        action['domain'] = [
            ('move_type', 'in', ('out_invoice', 'out_refund')),
            ('partner_id', '=', self.guest_id.id)
        ]
        action['context'] = {'default_move_type': 'out_invoice', 'move_type': 'out_invoice', 'journal_type': 'sale', 'search_default_unpaid': 1}
        return action


class InheriteHoteBookings(models.Model):
    _inherit = 'sale.order'

    register_ids = fields.One2many('hotel.register', 'booking_id', string="Booking Line")

    def action_noshow(self):
        print("no show action!!")
        self.bk_state = 'no_show'
        return

    # def action_check_in(self):
    #     for rec in self:
    #
    #         if(rec.bk_state in ['booked']):
    #             cat_int = 1
    #             if (rec.check_in_date and rec.check_out_date):
    #                 bedNights = (rec.check_out_date - rec.check_in_date).days
    #
    #             total_pax = 0
    #             for rt in rec.order_line:
    #                 total_pax = rt.product_id.adults + rt.product_id.childs + rt.product_id.infants
    #                 print('total pax', total_pax)
    #                 for x in range(total_pax):
    #                     line_vals2 = {
    #                         'name': rec.booking_name,
    #                         'arr_date': rec.check_in_date,
    #                         'dep_date': rec.check_out_date,
    #                         'meal_id': rt.product_id.meal_id.id,
    #                         'rm_cat_id': rt.product_id.room_category_id.id,
    #                         'booking_id': rec.id,
    #                         'booking_ref': rec.booking_ref,
    #                         'bk_method': rec.bk_method,
    #                         'category_int': cat_int,
    #                         'no_of_days': bedNights,
    #                         'identification_no': "none",
    #                         # 'country_id': _cn.id,
    #                         'reg_no': self.env['ir.sequence'].next_by_code('hotel.register') or _('New'),
    #
    #                     }
    #                     nrec = self.env['hotel.register'].create(line_vals2)
    #
    #             self.bk_state = 'check_in'
    #             return nrec
    #         else:
    #             raise ValidationError(
    #                 _('Booking is not valid for check-in!!'))

    def action_check_in(self):
        cat_id = 0
        meal_id = 0
        for rec in self:

            if(rec.total_guests_arrived <= 0 ):
                raise ValidationError(
                    _('Total gustes arrived must be grater than 0!!'))

            if not rec.allocated_room_id:
                raise ValidationError(
                    _('Select a room to proceed the check-in!!'))

            if(rec.bk_state in ['booked']):
                cat_int = 1

                # print('roomid', rec.allocated_room_id)
                # print('total_guests_arrived', rec.total_guests_arrived)

                # if (rec.check_in_date and rec.check_out_date):
                #     bedNights = (rec.check_out_date - rec.check_in_date).days

                total_pax_arrived = rec.total_guests_arrived

                for x in range(total_pax_arrived):

                    for rt in rec.order_line:
                        if(rt.product_id.is_room_type):
                            meal_id = rt.product_id.meal_id.id
                            cat_id = rt.product_id.room_category_id.id

                    line_vals2 = {
                        'name': rec.booking_name,
                        'arr_date': rec.check_in_date,
                        'dep_date': rec.check_out_date,
                        'meal_id': meal_id,
                        'rm_cat_id': cat_id,
                        'booking_id': rec.id,
                        'booking_ref': rec.booking_ref,
                        'bk_method': rec.bk_method,
                        'category_int': cat_int,
                        'no_of_days': rec.bed_nights,
                        'room_id': rec.allocated_room_id.id,
                        'identification_no': "none",
                        # 'guest_id': ptnr.id,
                        'country_id': rec.country_id.id,
                        'reg_no': self.env['ir.sequence'].next_by_code('hotel.register') or _('New'),
                    }
                    nrec = self.env['hotel.register'].create(line_vals2)


                self.bk_state = 'check_in'
                return nrec
            else:
                raise ValidationError(
                    _('Booking is not valid for check-in!!'))
