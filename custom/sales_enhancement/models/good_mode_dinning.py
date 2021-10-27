from odoo import models, fields, api, _


class GoodModeDinning(models.Model):
    _name = 'good.mode.dinning'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Good Mode Dinning'

    name = fields.Char()

    _sql_constraints = [('good_mode_dinning_name_uniq', 'unique(name)', "This name already exists !")]

