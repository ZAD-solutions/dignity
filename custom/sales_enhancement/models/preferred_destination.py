from odoo import models, fields, api, _


class SocialMedia(models.Model):
    _name = 'preferred.destination'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Preferred Destination'

    name = fields.Char()

    _sql_constraints = [('preferred_destination_name_uniq', 'unique(name)', "This name already exists !")]

