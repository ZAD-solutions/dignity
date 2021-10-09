from odoo import models, fields, api, _


class FavouriteSourceOfProtein(models.Model):
    _name = 'favourite.source.of.protein'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Favourite Source of Protein'

    name = fields.Char()

    _sql_constraints = [('favourite_source_of_protein_name_uniq', 'unique(name)', "This name already exists !")]

