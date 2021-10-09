from odoo import models, fields, api, _


class EnjoyMost(models.Model):
    _name = 'enjoy.most'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Enjoy Most'

    name = fields.Char()

    _sql_constraints = [('enjoy_most_name_uniq', 'unique(name)', "This name already exists !")]

