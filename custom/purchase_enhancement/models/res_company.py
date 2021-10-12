from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)
try:
    from num2words import num2words
except ImportError:
    _logger.debug('Cannot `import num2words`.')


class ResCompanyInherit(models.Model):
    _inherit = 'res.company'

    po_double_validation_amount = fields.Monetary(string='Purchase Manager Minimum Amount',
                                                  default=5000,
                                                  help="Minimum amount for which a double validation is required")

    ceo_po_validation_amount = fields.Monetary(string="CEO Minimum Amount", default=5000, readonly=False)
