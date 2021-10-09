from odoo import models, fields, api, _


class PreferredSeason(models.Model):
    _name = 'preferred.season'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Preferred Season'

    name = fields.Char()

    _sql_constraints = [('preferred_season_name_uniq', 'unique(name)', "This name already exists !")]

