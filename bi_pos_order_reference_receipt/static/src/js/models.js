odoo.define('bi_pos_order_reference_receipt.biOrderReferenceNo', function (require) {
"use strict";

var models = require('point_of_sale.models');
var { PosGlobalState, Order } = require('point_of_sale.models');
const Registries = require('point_of_sale.Registries');

const biOrderReferenceNo = (Order) => class biOrderReferenceNo extends Order {
    constructor(obj, options) {
        super(...arguments);
        this.order_reference_no = this.get_order_reference_no() || false;
    }
     init_from_JSON(json){
        super.init_from_JSON(...arguments);
        this.order_reference_no = json.order_reference_no;
    }
    set_order_reference_no(number){
        this.order_reference_no = number;
    }
    get_order_reference_no() {
        return this.order_reference_no;
    }
    export_as_JSON() {
        const json = super.export_as_JSON(...arguments);
        json.order_reference_no = this.order_reference_no;
        return json
    }
    export_for_printing() {
        const json = super.export_for_printing(...arguments);
        json.order_reference_no = this.get_order_reference_no();
        return json;
    }
}
Registries.Model.extend(Order, biOrderReferenceNo);
});