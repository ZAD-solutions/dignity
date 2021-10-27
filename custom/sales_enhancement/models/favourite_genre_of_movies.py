from odoo import models, fields, api, _


class FavouriteGenreOfMovies(models.Model):
    _name = 'favourite.genre.of.movies'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Favourite Genre of Movies'

    name = fields.Char()

    _sql_constraints = [('favourite_genre_of_movies_name_uniq', 'unique(name)', "This name already exists !")]

