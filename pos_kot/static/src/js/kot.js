console.log("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHh")
odoo.define('pos_kot.DemoButton', function(require) {
'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');


    class CustomDemoButtons extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }
        is_available() {
            const order = this.env.pos.get_order();
            return order
        }
        async onClick() {
            const order = this.env.pos.get_order();
            if (order.get_orderlines().length > 0) {
                this.trigger('close-popup');
                await this.showTempScreen('Kot_Screen');
            } else {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t('Nothing to Print'),
                    body: this.env._t('There are no order lines'),
                });
            }
         }
    }
    CustomDemoButtons.template = 'CustomDemoButtons';

    ProductScreen.addControlButton({
        component: CustomDemoButtons,
        condition: function() {
            return this.env.pos;
        },
   });
    Registries.Component.add(CustomDemoButtons);
    return CustomDemoButtons;

});
