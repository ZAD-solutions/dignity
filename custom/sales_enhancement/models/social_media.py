from odoo import models, fields, api, _


class SocialMedia(models.Model):
    _name = 'social.media'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Social Media'

    name = fields.Char()

    _sql_constraints = [('social_media_name_uniq', 'unique(name)', "This name already exists !")]

