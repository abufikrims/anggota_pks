from datetime import datetime
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class account_fiscalyear(models.Model):
    _inherit        = 'account.fiscalyear'

    harga_komponen  = fields.One2many('fiscalyear.harga', 'fiscalyear_id', 'Komponen Price')


class fiscalyear_harga(models.Model):
    _name           = "fiscalyear.harga"

    fiscalyear_id   = fields.Many2one('account.fiscalyear', 'Tahun Periodik', required=True, ondelete='cascade')
    name            = fields.Many2one('komponen.usaha', 'Komponen', required=True)
    price_unit      = fields.Float('Harga', digits=dp.get_precision('Product Price'))

class komponen_usaha(models.Model):
    _name           = "komponen.usaha"

    name            = fields.Char('Nama', required=True)
    type            = fields.Selection((('iwai', 'IWAI'), ('tapilu', 'TAPILU'), ('zakat', 'ZAKAT'), ('infaq', 'Infaq'), ('other', 'Lain-Lain')), 'Tipe', required=True)
    tujuan          = fields.Selection((('partai','Partai'), ('ziswaf','ZISWAF'), ('sosial','Sosial Masyarakat')), 'Kategori/Tujuan', required=True)
    cicil           = fields.Selection((('credit', 'Credit'), ('cash','Cash')), 'Payment', required=True, default='cash')
    active          = fields.Boolean('Active', default=True)
    product_id      = fields.Many2one('product.product', 'Produk', required=True)

class res_partner_harga(models.Model):
    _name           = "anggota_pks.harga"

    partner_id      = fields.Many2one('res.partner', 'Anggota', required=True, ondelete='cascade' )
    name            = fields.Many2one('komponen.usaha', 'Komponen', required=True)
    disc_amount     = fields.Integer('Disc Amount')
    disc_persen     = fields.Integer('Disc Percent')
    notes           = fields.Char('Keterangan')

class account_invoice(models.Model):
    _inherit        = 'account.invoice'

    @api.one
    @api.depends('invoice_line_ids')
    def _add_line(self):
        self.info_line = ', '.join([line.name for line in self.invoice_line_ids])

    #anggota         = fields.Boolean('Anggota')
    #no_kta          = fields.Char(string='No. KTA')
    
    cicil           = fields.Selection((('credit', 'Credit'), ('cash','Hard Cash')), 'Pembayaran', default='cash')
    fiscalyear_id   = fields.Many2one('account.fiscalyear', 'Tahun Ajaran', related='partner_id.fiscalyear_id', readonly=True, store=True)
    komponen_id     = fields.Many2one('komponen.usaha', 'Komponen', readonly=True, states={'draft': [('readonly', False)]})
    period_id       = fields.Many2one('account.period', string='Force Period', copy=False, readonly=True, states={'draft': [('readonly', False)]})

    info_line       = fields.Char(compute='_add_line', string='Invoice Line')

    _sql_constraints = [('invoice_uniq', 'unique(komponen_id, partner_id, period_id)', 'Invoice sudah pernah dibuat !')]

    # @api.onchange('orangtua_id')
    # def onchange_orangtua_id(self):
    #     if self.partner_id:
    #         data = {'orangtua_id': self.partner_id.orangtua_id.id, 'fiscalyear_id': self.partner_id.fiscalyear_id.id}
    #         self.update(data)

    @api.onchange('komponen_id')
    def onchange_komponen_id(self):
        if self.komponen_id:
            product = []; harga = {}
            for o in self.partner_id.fiscalyear_id.harga_komponen:
                harga[o.name.product_id.id] = o.price_unit

            i = self.komponen_id.product_id
            price = i.lst_price
            if harga.has_key(i.id):
                price = harga[i.id]
            product.append({
                            'name'      : i.partner_ref,
                            'product_id': i.id,
                            'uos_id'    : i.uom_id.id,
                            'price_unit': price,
                            'quantity'  : 1,
                            'account_id': i.categ_id.property_account_income_categ_id.id
            })

            self.update({'invoice_line_ids': product, 'cicil': self.komponen_id.cicil})

class account_invoice_line_inherit(models.Model):
    _inherit            = 'account.invoice.line'
    
    discount_amount     = fields.Float(string='Discount Amount')