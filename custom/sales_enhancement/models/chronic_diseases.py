from odoo import models, fields, api, _


class ChronicDiseases(models.Model):
    _name = 'chronic.diseases'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Chronic Diseases'

    name = fields.Char(string="Name", required=True, copy=False, track_visibility='onchange', )

    _sql_constraints = [('chronic_diseases_name_uniq', 'unique(name)', "This name already exists !")]
