from odoo import models, fields, api, _


class Pastime(models.Model):
    _name = 'pastime'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Pastime'

    name = fields.Char(string="Name", required=True, copy=False, track_visibility='onchange', )
    active = fields.Boolean(default=True, )

    _sql_constraints = [('pastime_name_uniq', 'unique(name)', "This name already exists !")]
