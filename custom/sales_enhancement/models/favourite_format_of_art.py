from odoo import models, fields, api, _


class FavouriteFormatOfArt(models.Model):
    _name = 'favourite.format.of.art'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Favourite Format of Art'

    name = fields.Char()

    _sql_constraints = [('favourite_format_of_art_name_uniq', 'unique(name)', "This name already exists !")]

