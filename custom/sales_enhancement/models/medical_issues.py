from odoo import models, fields, api, _


class MedicalIssues(models.Model):
    _name = 'medical.issues'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'type'
    _description = 'Medical Issues'

    type = fields.Selection([('medical_issues', 'Medical Issues'),
                             ('allergies', 'Allergies'),
                             ('surgery', 'Surgery')])
    date = fields.Date()
    more_info = fields.Char()
    partner_id = fields.Many2one('res.partner')
    lead_id = fields.Many2one('crm.lead')

