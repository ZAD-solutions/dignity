from odoo import models, fields, api, _


class PreferredChocolate(models.Model):
    _name = 'preferred.chocolate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Preferred Chocolate'

    name = fields.Char()

    _sql_constraints = [('preferred_chocolate_name_uniq', 'unique(name)', "This name already exists !")]

