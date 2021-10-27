from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)
try:
    from num2words import num2words
except ImportError:
    _logger.debug('Cannot `import num2words`.')


class PurchaseOrderInherit(models.Model):
    _inherit = 'purchase.order'

    state = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to_approve', 'Purchase Manager Approve'),
        ('ceo_approve', 'CEO Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    def button_confirm(self):
        for order in self:
            po_manager_validation = self.env.company.currency_id._convert(
                order.company_id.po_double_validation_amount, order.currency_id, order.company_id,
                order.date_order or fields.Date.today())
            ceo_manager_validation = order.env.company.currency_id._convert(
                order.company_id.ceo_po_validation_amount, order.currency_id, order.company_id,
                order.date_order or fields.Date.today())

            order._add_supplier_to_product()
            if po_manager_validation and ceo_manager_validation and order.company_id.po_double_validation == 'two_step':
                if order.amount_total < po_manager_validation:
                    order.button_approve()
                elif po_manager_validation <= order.amount_total < ceo_manager_validation:
                    if order.state == 'to_approve' and self.env.user.has_group('purchase.group_purchase_manager'):
                        order.button_approve()
                    elif order.state == 'to_approve' and not self.env.user.has_group('purchase.group_purchase_manager'):
                        raise UserError('Purchase Manager only has access to confirm this PO')
                    else:
                        order.state = 'to_approve'
                elif order.amount_total >= ceo_manager_validation:
                    if order.state == 'draft':
                       order.state = 'to_approve'
                    elif order.state == 'to_approve' and self.env.user.has_group('purchase.group_purchase_manager'):
                        order.state = 'ceo_approve'
                    elif order.state == 'to_approve' and not self.env.user.has_group('purchase.group_purchase_manager'):
                        raise UserError('Purchase Manager only has access to confirm this PO')
                    elif order.state == 'ceo_approve' and self.env.user.has_group('purchase_enhancement.ceo_group'):
                        order.button_approve()
                    elif order.state == 'ceo_approve' and not self.env.user.has_group('purchase_enhancement.ceo_group'):
                        raise UserError('CEO only has access to confirm this PO')
                    else:
                        order.state = 'ceo_approve'
            else:
                order.button_approve()

            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
        return True