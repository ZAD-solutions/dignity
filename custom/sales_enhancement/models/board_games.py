from odoo import models, fields, api, _


class BoardGames(models.Model):
    _name = 'board.games'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Board Games'

    name = fields.Char()

    _sql_constraints = [('board_games_name_uniq', 'unique(name)', "This name already exists !")]

