from odoo import models, fields, api, _


class AgeGroups(models.Model):
    _name = 'age.groups'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Age Groups'

    name = fields.Char(string="Name", required=True, copy=False, track_visibility='onchange', )
    active = fields.Boolean(default=True, )

    _sql_constraints = [('age_groups_name_uniq', 'unique(name)', "This name already exists !")]
