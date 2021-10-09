from odoo import models, fields, api, _


class FavouriteMusic(models.Model):
    _name = 'favourite.music'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Favourite Music'

    name = fields.Char()

    _sql_constraints = [('favourite_music_name_uniq', 'unique(name)', "This name already exists !")]

