from odoo import models, fields, api, _


class FavouriteSportToEngage(models.Model):
    _name = 'favourite.sport.to.engage'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Favourite Sport to Engage'

    name = fields.Char()

    _sql_constraints = [('favourite_sport_to_engage_name_uniq', 'unique(name)', "This name already exists !")]

