from odoo import models, fields, api, _


class FavouriteSportToWatch(models.Model):
    _name = 'favourite.sport.to.watch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Favourite Sport to Watch'

    name = fields.Char()

    _sql_constraints = [('favourite_sport_to_watch_name_uniq', 'unique(name)', "This name already exists !")]

