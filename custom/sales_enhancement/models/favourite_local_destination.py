from odoo import models, fields, api, _


class FavouriteLocalDestination(models.Model):
    _name = 'favourite.local.destination'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Favourite Local Destination'

    name = fields.Char()

    _sql_constraints = [('favourite_local_destination_name_uniq', 'unique(name)', "This name already exists !")]

