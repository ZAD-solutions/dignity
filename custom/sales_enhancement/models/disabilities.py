from odoo import models, fields, api, _


class Disabilities(models.Model):
    _name = 'disabilities'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Disabilities'

    name = fields.Char(string="Name", required=True, copy=False, track_visibility='onchange', )
    active = fields.Boolean(default=True, )

    _sql_constraints = [('disabilities_name_uniq', 'unique(name)', "This name already exists !")]
