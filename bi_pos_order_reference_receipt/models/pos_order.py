from odoo import models, api, fields, tools
import logging
_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = 'pos.order'


    @api.model
    def create_from_ui(self, orders, draft=False):

        order_ids = []
        for order in orders:
            existing_order = False
            if 'server_id' in order['data']:
                existing_order = self.env['pos.order'].search(['|', ('id', '=', order['data']['server_id']),
                                                               ('pos_reference', '=', order['data']['name'])], limit=1)

            if (existing_order and existing_order.state == 'draft') or not existing_order:
                order_ids.append(self._process_order(order, draft, existing_order))
        return self.env['pos.order'].search_read(domain=[('id', 'in', order_ids)],
                                                 fields=['id', 'name', 'pos_reference', 'account_move'], load=False)