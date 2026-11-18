odoo.define('bi_pos_order_reference_receipt.BiPaymentScreen', function(require) {

	const PosComponent = require('point_of_sale.PosComponent');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const { useState } = owl;
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const { Orderline } = require('point_of_sale.models');
    var core = require('web.core');
    var _t = core._t;
	var utils = require('web.utils');

	const BiPaymentScreen = (ProductScreen) => class extends ProductScreen {
        setup() {
            super.setup();
		}
		async _finalizeValidation() {
            if ((this.currentOrder.is_paid_with_cash() || this.currentOrder.get_change()) && this.env.pos.config.iface_cashdrawer) {
                this.env.proxy.printer.open_cashbox();
            }
            this.currentOrder.initialize_validation_date();
            this.currentOrder.finalized = true;
            let syncOrderResult, hasError;
            try {
                syncOrderResult = await this.env.pos.push_single_order(this.currentOrder);
                this.env.pos.get_order().set_order_reference_no(syncOrderResult[0].name)
                if (this.currentOrder.is_to_invoice()) {
                    if (syncOrderResult.length) {
                        await this.env.legacyActionManager.do_action('account.account_invoices', {
                            additional_context: {
                                active_ids: [syncOrderResult[0].account_move],
                            },
                        });
                    } else {
                        throw { code: 401, message: 'Backend Invoice', data: { order: this.currentOrder } };
                    }
                }
                if (syncOrderResult.length && this.currentOrder.wait_for_push_order()) {
                    const postPushResult = await this._postPushOrderResolve(
                        this.currentOrder,
                        syncOrderResult.map((res) => res.id)
                    );
                    if (!postPushResult) {
                        this.showPopup('ErrorPopup', {
                            title: this.env._t('Error: no internet connection.'),
                            body: this.env._t('Some, if not all, post-processing after syncing order failed.'),
                        });
                    }
                }
            } catch (error) {
                if (error.code == 700 || error.code == 701)
                    this.error = true;
                if ('code' in error) {
                    await this._handlePushOrderError(error);
                } else {
                    if (isConnectionError(error)) {
                        this.showPopup('OfflineErrorPopup', {
                            title: this.env._t('Connection Error'),
                            body: this.env._t('Order is not synced. Check your internet connection'),
                        });
                    } else {
                        throw error;
                    }
                }
            } finally {
                this.showScreen(this.nextScreen);
                this.env.pos.db.remove_unpaid_order(this.currentOrder);
                if (!hasError && syncOrderResult && this.env.pos.db.get_orders().length) {
                    const { confirmed } = await this.showPopup('ConfirmPopup', {
                        title: this.env._t('Remaining unsynced orders'),
                        body: this.env._t(
                            'There are unsynced orders. Do you want to sync these orders?'
                        ),
                    });
                    if (confirmed) {
                        this.env.pos.push_orders();
                    }
                }
            }
        }
	}
	Registries.Component.extend(PaymentScreen, BiPaymentScreen);
	return PaymentScreen;
});