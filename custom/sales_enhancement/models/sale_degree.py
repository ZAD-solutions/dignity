from odoo import models, fields, api, _


class SaleDegree(models.Model):
    _name = 'sale.degree'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Degrees'

    name = fields.Char(string="Degree Name", required=True, copy=False, track_visibility='onchange', )
    active = fields.Boolean(default=True, )

    _sql_constraints = [('degree_name_uniq', 'unique(name)', "This degree name already exists !")]
