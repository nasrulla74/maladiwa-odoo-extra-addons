odoo.define('bi_pos_order_reference_receipt.ReprintReceiptButton', function(require) {
	'use strict';

	const ReprintReceiptButton = require('point_of_sale.ReprintReceiptButton');
	const Registries = require('point_of_sale.Registries');
	const session = require('web.session');

	const PosOrderReferenceReprintReceiptButton = ReprintReceiptButton =>
		class extends ReprintReceiptButton {
			async _onClick() {
	            if (!this.props.order) return;
	            const result = await this.rpc({
	                model: 'pos.order',
	                method: 'search_read',
	                domain: [['pos_reference', '=', this.props.order.name]],
	                fields: ['name'],
	                context: session.user_context,
	            });
	            this.props.order.set_order_reference_no(result[0].name || false);
	            this.showScreen('ReprintReceiptScreen', { order: this.props.order });
	        }
		};
	Registries.Component.extend(ReprintReceiptButton, PosOrderReferenceReprintReceiptButton);

	return ReprintReceiptButton;
});