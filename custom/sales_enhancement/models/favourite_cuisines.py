from odoo import models, fields, api, _


class FavouriteCuisines(models.Model):
    _name = 'favourite.cuisines'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Favourite Cuisines'

    name = fields.Char()

    _sql_constraints = [('favourite_cuisines_name_uniq', 'unique(name)', "This name already exists !")]

