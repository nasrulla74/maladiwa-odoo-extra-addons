from odoo import models, fields ,api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    kot = fields.Boolean(string='Enable Kitchen Order Print')

class ResPosConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    kot = fields.Boolean(related='pos_config_id.kot', readonly=False, store=True)