/** @odoo-module */

import Registries from "point_of_sale.Registries"
import PartnerListScreen from "point_of_sale.PartnerListScreen"
const { onWillStart } = owl

var utils = require('web.utils');

const PartnerListScreenInherit = (partner_list_screen) => class extends partner_list_screen {
    setup(){
        super.setup()
        console.log("==========Inherited Partner List Screen!!")
        console.log("db log", this.env.pos.db)
        this.guest_list = []
        onWillStart(async ()=> {
            const data = await this.env.services.rpc({
                    'model': 'res.partner',
                    'method': 'search_read',
                    'kwargs': {
                        'domain': [['is_guest', '=', true], ['x_is_checked_out', '=', false]],
                        'fields': ['is_guest','x_is_checked_out','x_room_no','name','city','barcode','email','lang','mobile','parent_name','phone','country_id','property_account_position_id','property_product_pricelist','state_id','street','vat','write_date','zip']
                    }
                })
                this.guest_list = data
                console.log('data', data)

            })

    }

    get partners() {
        let res;
        if (this.state.query && this.state.query.trim() !== '') {
            const result = this.guest_list.filter((p) => {
                return p.name.toString().toLowerCase().includes(this.state.query.trim().toString().toLowerCase())
            })

            this.guest_list = result

//            res = this.env.pos.db.search_partner(this.state.query.trim());
            res = this.guest_list

        } else {
            res = this.guest_list
        }

        res.sort(function (a, b) { return (a.phone || '').localeCompare(b.phone || '') });
            // the selected partner (if any) is displayed at the top of the list
        if (this.state.selectedPartner) {
            let indexOfSelectedPartner = res.findIndex( partner =>
               partner.id === this.state.selectedPartner.id
            );
            if (indexOfSelectedPartner !== -1) {
                res.splice(indexOfSelectedPartner, 1);
            }
            res.unshift(this.state.selectedPartner);
        }
        return res
    }

}

Registries.Component.extend(PartnerListScreen, PartnerListScreenInherit)