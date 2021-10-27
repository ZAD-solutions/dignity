from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)
try:
    from num2words import num2words
except ImportError:
    _logger.debug('Cannot `import num2words`.')


class ResConfigSettingsInherit(models.TransientModel):
    _inherit = 'res.config.settings'

    po_double_validation_amount = fields.Monetary(related='company_id.po_double_validation_amount',
                                                  string="Purchase Manager Minimum Amount",
                                                  currency_field='company_currency_id', readonly=False)
    ceo_po_validation_amount = fields.Monetary(related='company_id.ceo_po_validation_amount',
                                               string="CEO Minimum Amount",
                                               currency_field='company_currency_id', readonly=False)
