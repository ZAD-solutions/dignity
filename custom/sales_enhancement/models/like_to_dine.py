from odoo import models, fields, api, _


class LikeToDine(models.Model):
    _name = 'like.to.dine'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Like to Dine'

    name = fields.Char()

    _sql_constraints = [('like_to_dine_name_uniq', 'unique(name)', "This name already exists !")]

