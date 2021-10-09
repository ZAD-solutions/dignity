from odoo import models, fields, api, _


class FootballClub(models.Model):
    _name = 'football.club'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Football Club'

    name = fields.Char()

    _sql_constraints = [('football_club_name_uniq', 'unique(name)', "This name already exists !")]

