from odoo import models, fields, api, _


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    sale_order_type = fields.Selection([('air_conditions','تكيفات'),('refrigerators','ثلاجات'),('ice_makers','مصانع ثلج'),('water_filters','فلاتر مياه'),('other','أخري')],'Type',required=True)

    # @api.model
    # def _get_default_type(self):
    #     for rec in self:
    #         if rec.sale_order_type=='air_conditions':
    #             rec.sale_order_type_id = self.env.ref("elashry_sales.sale_order_type_air_conditions").id
    #         elif rec.sale_order_type=='refrigerators':
    #             rec.sale_order_type_id = self.env.ref("elashry_sales.sale_order_type_ref").id
    #         elif rec.sale_order_type == 'ice_makers':
    #             rec.sale_order_type_id = self.env.ref("elashry_sales.sale_order_type_ice").id
    #         elif rec.sale_order_type == 'water_filters':
    #             rec.sale_order_type_id = self.env.ref("elashry_sales.sale_order_type_filters").id
    #         else:
    #             rec.sale_order_type_id = False

    sale_order_type_id = fields.Many2one("sale.order.type",string='النوع',)

    date_day = fields.Char(compute="_compute_date_day")

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('finance_manager', 'Financial Manager Approval'),
        ('owner_manager', 'Owner Approval'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft', tracking=True)

    quotation_rules_prices = fields.Text("الاسعار")
    quotation_rules_import = fields.Text("التوريد")
    quotation_rules_meter_price = fields.Text("سعر متر المواسير")
    quotation_rules_payment = fields.Text("السداد")
    quotation_rules_period = fields.Text("مدة العرض")
    quotation_rules_delivery = fields.Text("التسليم")
    quotation_rules_warranty = fields.Text("الضمان")

    cash_numbers = fields.Char(compute="_compute_cash_number")

    @api.depends("invoice_ids")
    def _compute_cash_number(self):
        for order in self:
            cash=""
            if order.invoice_ids:

                for invoice in order.invoice_ids:
                    payment = self.env['account.payment'].search([('invoice_ids', 'in', invoice.id)])
                    if payment:
                        cash += "," + str(payment.name)

                    else:
                        for line in invoice.line_ids:

                            if line.statement_line_id:
                                cash += "," + str(line.statement_line_id.statement_id.name)
                            elif line.full_reconcile_id:
                                reconcillation = self.env['account.move.line'].search(
                                    [('full_reconcile_id', '=', line.full_reconcile_id.id), ('id', '!=', line.id)],
                                    limit=1)
                                if reconcillation:
                                    cash += "," + str(reconcillation.move_id.name)

            order.cash_numbers = cash


    @api.depends("date_order")
    def _compute_date_day(self):
        date_day=""
        for rec in self:
            date_day = rec.date_order.strftime('%A')

            if date_day=='Friday':
                rec.date_day = "الجمعة"

            if date_day=='Saturday':
                rec.date_day = "السبت"

            if date_day=='Sunday':
                rec.date_day = "الأحد"

            if date_day=='Monday':
                rec.date_day = "الإثنين"

            if date_day=='Tuesday':
                rec.date_day = "الثلاثاء"

            if date_day=='Wednesday':
                rec.date_day = "الأربعاء"

            if date_day=='Thursday':
                rec.date_day = "الخميس"



    def send_to_approve(self):
        for order in self:
            check_price=False
            for line in order.order_line:
                if line.price_unit < line.product_id.standard_price:
                    check_price=True

            if check_price:
                order.write({'state': 'owner_manager'})
                group_obj = self.env.ref('elashry_sales.group_owner')
                order._notify_group(group_obj)
                order._notify_creator("Waiting for Owner Approval")


            else:
                order.write({'state': 'finance_manager'})
                group_obj = self.env.ref('elashry_sales.group_finance_approve_manager')
                order._notify_group(group_obj)

    def finance_manager_approve(self):
        for order in self:
            order.write({'state': 'owner_manager'})
            group_obj = self.env.ref('elashry_sales.group_owner')
            order._notify_group(group_obj)
            order._notify_creator("approved by Finance Manager and Waiting for Owner Approval")


    def finance_manager_reject(self):
        for order in self:
            order.write({'state': 'draft'})

            order._notify_creator("Rejected by Finance Manager")

    def owner_approve(self):
        for order in self:
            order.action_confirm()
            order._notify_creator("Confirmed and Approved by Owner")


    def owner_reject(self):
        for order in self:
            order.write({'state': 'draft'})
            order._notify_creator("Rejected by Owner")

    def generate_url(self):
        """
        Build the URL to the record's form view.
          - Base URL + Database Name + Record ID + Model Name

        :param self: any Odoo record browse object (with access to env, _cr, and _model)
        :return: string with url
        """

        self.ensure_one()
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        if base_url and base_url[-1:] != '/':
            base_url += '/'
        db = self._cr.dbname
        return "{}web?db={}#id={}&view_type=form&model={}".format(base_url, db, self.id, self._name)

    def _notify_group(self, group_obj):

        for order in self:

            partner_ids = []
            for user in group_obj.users:
                partner_ids.append(user.partner_id.id)

                # if len(partner_ids) > 0:
            body = 'SO#<a href="%s">%s</a> is added and Waiting for your approval.' % (order.generate_url(), order.name)
            subject = _('Sale Order Approval.')

            channel_id = self.env.ref("mail.channel_all_employees")
            channel_id.message_post(
                subject=subject,
                body=body,
                message_type='notification',
                subtype='mail.mt_comment',
                partner_ids=partner_ids
            )

    def _notify_creator(self,state):

        for order in self:


            body = 'SO#<a href="%s">%s</a> is.%s' % (order.generate_url(), order.name,state)
            subject = _('Sale Order Approval.')

            channel_id = self.env.ref("mail.channel_all_employees")
            channel_id.message_post(
                subject=subject,
                body=body,
                message_type='notification',
                subtype='mail.mt_comment',
                partner_id=order.create_uid.partner_id.id
            )
class SaleOrderLine(models.Model):
    _inherit="sale.order.line"

    def _prepare_invoice_line(self):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        price_unit=self.price_unit
        total_amount_eng_f=0
        total_amount_warranty=0
        total_warranty_taxes=0
        
        
        if self.order_id.sale_order_type=='air_conditions':
            stock_moves = self.env['stock.move'].search([('sale_line_id', '=', self.id)])

            if stock_moves:
                for move_line in stock_moves.move_line_ids:
                    total_amount_eng_f += move_line.amount_eng_f
                    total_amount_warranty += move_line.amount_warranty
                    total_warranty_taxes += move_line.warranty_taxes

                price_unit=price_unit  - (total_amount_eng_f+total_amount_warranty+total_warranty_taxes)/self.qty_to_invoice
            
                price_unit = price_unit/1.14
            

        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'sales_amount_eng_f':total_amount_eng_f/self.qty_to_invoice,
            'sales_amount_warranty':total_amount_warranty/self.qty_to_invoice,
            'sales_warranty_taxes':total_warranty_taxes/self.qty_to_invoice,
            'price_unit': price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
            
        }
        if self.display_type:
            res['account_id'] = False
        return res
