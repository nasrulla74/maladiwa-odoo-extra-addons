# -*- coding: utf-8 -*-
from odoo import fields, api, models, _
from odoo.exceptions import ValidationError
from datetime import datetime, date



class HotelBookingAddProduct(models.TransientModel):
    _name = 'add.roomtype.wizard'
    _description = 'Add Products Extend'

    @api.model
    def default_get(self, fields):
        res = super(HotelBookingAddProduct, self).default_get(fields)
        if (self.env.context.get('active_id')):
            bk_id = self.env.context.get('active_id')
            result = self.env['sale.order'].browse(bk_id)
            hotel_id = result.hotel_id.id
            res['hotel_id'] = hotel_id
            res['booking_id'] = bk_id
            return res

    hotel_id = fields.Many2one('hotel.hotel', string="Hotel", required=True)
    room_cate_id = fields.Many2one('room.category', string="Room Category",  required=True, domain="[('hotel_id', '=', hotel_id)]")
    meal_id = fields.Many2one('hotel.meal', string="Meal", default=4)
    adults = fields.Integer('Adults', required=True, default=2)
    childs = fields.Integer('Childs')
    infants = fields.Integer('Infants')
    total_amount = fields.Integer('Total Amount Incl.GST')
    booking_id = fields.Integer('Booking Id')

    def action_room_type(self):
        print("action_room_type action click!!")
        hotel_id = self.hotel_id.id
        room_cate_id = self.room_cate_id.id
        meal_id = self.meal_id.id
        adults = self.adults
        childs = self.childs
        infants = self.infants
        total_amount = self.total_amount

        hotel_name = self.hotel_id.name
        cat_name = self.room_cate_id.name
        meal_name = self.meal_id.name
        booking_id = self.booking_id


        domain = [('hotel_id', '=', hotel_id), ('room_category_id', '=', room_cate_id), ('meal_id', '=', meal_id), ('adults', '=', adults), ('childs', '=', childs), ('infants', '=', infants)]
        rm_type_id = self.env['product.product'].sudo().search(domain)

        if(rm_type_id):
            total_amount_exc_tax = total_amount
            self.env['sale.order.line'].create({'product_id': rm_type_id.id, 'order_id': booking_id, 'price_unit': total_amount_exc_tax})
        else:
            name_text = hotel_name + "/" + cat_name + "/" + meal_name + " | " + str(
                adults) + " Adults + (" + str(childs) + " Child, " + str(infants) + " Infants)"
            room_type_id = self.env['product.product'].create({'name': name_text,'hotel_id': hotel_id, 'room_category_id': room_cate_id, 'room_type_name': hotel_name, 'meal_id': meal_id, 'is_room_type': True, 'adults': adults, 'childs': childs, 'infants': infants})

            total_amount_exc_tax = total_amount
            self.env['sale.order.line'].create(
                {'product_id': room_type_id.id, 'order_id': booking_id, 'price_unit': total_amount_exc_tax})





