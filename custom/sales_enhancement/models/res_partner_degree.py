# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta


class ResPartnerDegree(models.Model):
    _name = 'res.partner.degree'
    _rec_name = 'degree_id'
    _description = "Partner Degrees"

    degree_id = fields.Many2one('sale.degree', required=True, )
    institutions_id = fields.Many2one('institutions', required=True, )
    date = fields.Date()
    partner_id = fields.Many2one('res.partner', )