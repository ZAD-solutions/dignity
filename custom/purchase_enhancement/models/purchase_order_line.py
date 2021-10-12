from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
import logging


class PurchaseOrderLineInherit(models.Model):
    _inherit = 'purchase.order.line'

