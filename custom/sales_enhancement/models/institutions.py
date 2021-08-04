from odoo import models, fields, api, _


class Institutions(models.Model):
    _name = 'institutions'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Institutions'

    name = fields.Char(string="Name", required=True, copy=False, track_visibility='onchange', )
    active = fields.Boolean(default=True, )

    _sql_constraints = [('institutions_name_uniq', 'unique(name)', "This Institutions name already exists !")]
