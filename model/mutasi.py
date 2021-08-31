from odoo import api, fields, models


class mutasiPKS(models.Model):
    _name               = 'mutasi_pks'
    _description        = 'Tabel Mutasi Anggota PKS'

    name                = fields.Char(string="No. Referensi",  help="", readonly=True, default='Auto')
    tanggal             = fields.Date(string='Tanggal Mutasi', required=True)
    anggota_id          = fields.Many2one(comodel_name='pks_anggota', string='Nama Anggota')
    
    jns_mutasi          = fields.Selection(string='Jenis Mutasi', selection=[('in', 'Mutasi Masuk'), ('out', 'Mutasi Keluar'),], required=True)
    
    propinsi_id         = fields.Many2one(comodel_name='ref.propinsi', string='Propinsi')
    kota_id             = fields.Many2one(comodel_name='ref.kota', string='Kabupaten/Kota')
    kecamatan_id        = fields.Many2one(comodel_name='ref.kecamatan', string='Kecamatan')
    desa_id             = fields.Many2one(comodel_name='ref.desa', string='Desa/Kelurahan')
    alamat              = fields.Char(string='Alamat Lengkap')
    state               = fields.Selection(string='Status', selection=[('draft', 'Draft'), ('confirm', 'Konfirmasi'),], default='draft')
    

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('mutasi_pks')
        return super(mutasiPKS, self).create(vals)

    def action_confirm(self):
        self.state = 'confirm'
        cari_anggota = self.env['pks_anggota'].search([('id', '=', self.anggota_id.id)])
        if cari_anggota:
            cari_anggota.write({'mutasi_id':self.id, 'active':(self.jns_mutasi=='in')})
            # if self.jns_mutasi=='out':
            #     cari_anggota.write({'mutasi_id':self.id, 'active':False})
            # else:
            #     cari_anggota.write({'mutasi_id':self.id, 'active':True})

    def action_draft(self):
        self.state = 'draft'
    
    
    
