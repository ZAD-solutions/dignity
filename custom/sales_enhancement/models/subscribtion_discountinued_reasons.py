from odoo import models, fields, api, _


class SubscriptionDiscontinuedReasons(models.Model):
    _name = 'subscription.discontinued.reasons'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'name'
    _description = 'Subscription Discontinued Reasons'

    name = fields.Char(string="Name", required=True, copy=False, track_visibility='onchange', )
    active = fields.Boolean(default=True, )

    _sql_constraints = [('subscription.discontinued.reasons_name_uniq', 'unique(name)', "This name already exists !")]
