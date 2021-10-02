#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pks_anggota(models.Model):

    _name               = "pks_anggota"
    _description        = "Pendataan Anggota PKS"
    _inherits           = {'res.partner': 'partner_id'}
    _inherit            = ['mail.thread', 'mail.activity.mixin']

    partner_id          = fields.Many2one("res.partner", string='Partner ID', required=True, ondelete="cascade")
    nik                 = fields.Char( string="NIK", required=True, help="")
    jns_kelamin         = fields.Selection(selection=[('laki-laki','Laki-Laki'),('perempuan','Perempuan')],  string="Jenis kelamin", required=True, help="")
    tmp_lahir           = fields.Char( string="Tmp lahir",  help="", track_visibility='onchange')
    tgl_lahir           = fields.Date( string="Tgl lahir",  help="")
    status_kawin        = fields.Selection(selection=[('menikah','Menikah'),('janda','Janda'),('duda','Duda'),('belum menikah','Belum Menikah')],  string="Status Kawin", required=True, help="")

    # Data Alamat
    #nama jalan dan rt_rw menggunakan field street dan street2 di model res.partner
    propinsi_id         = fields.Many2one(comodel_name='ref.propinsi', string='Propinsi')
    kota_id             = fields.Many2one(comodel_name='ref.kota', string='Kabupaten/Kota')
    kecamatan_id        = fields.Many2one(comodel_name='ref.kecamatan', string='Kecamatan')
    desa_id             = fields.Many2one(comodel_name='ref.desa', string='Desa/Kelurahan')


    #Jika Alamat Tinggal beda dengan KTP
    tg_sesuai_ktp       = fields.Selection(string='Tempat Tinggal', selection=[('1', 'Sesuai KTP'), ('0', 'Beda Lokasi Tinggal'),], required=True, default="0")
    
    tg_street           = fields.Char(string='Nama Jalan')
    tg_street2          = fields.Char(string='RT/RW')
    tg_propinsi_id      = fields.Many2one(comodel_name='ref.propinsi', string='Propinsi')
    tg_kota_id          = fields.Many2one(comodel_name='ref.kota', string='Kabupaten/Kota')
    tg_kecamatan_id     = fields.Many2one(comodel_name='ref.kecamatan', string='Kecamatan')
    tg_desa_id          = fields.Many2one(comodel_name='ref.desa', string='Desa/Kelurahan')

    # @api.model
    # def get_kota_default(self):
    #     return self['res.company'][1].kota_id

    amanah_struktural   = fields.Selection(selection=[('dpp','DPP'),('dpw','DPW'),('dpd','DPD'),('dpc','DPC'),('dpra','DPRa')],  string="Amanah Struktural",  help="")
    jabatan_struktural  = fields.Char( string="Jabatan Struktural",  help="")
    jabatan_yayasan     = fields.Char(string='Jabatan Yayasan', help='')
    amanah              = fields.Many2one(comodel_name='ref.kecamatan', string='Amanah', domain=lambda self:[('kota_id','=', self.env['res.company'].search([('id','=',1)]).kota_id.id)])

   
    
    jabatan_masyarakat  = fields.Char( string="Jabatan Masyarakat",  help="")
    ada_kta             = fields.Selection(string='Sudah Ber KTA', selection=[('1', 'YA'), ('0', 'TIDAK/BELUM'),], required=True, default='0')
    no_kta              = fields.Char( string="No KTA",  help="")

    # Data Liqo' / UPA
    halaqoh_id          = fields.Many2one(comodel_name='kelas_tarbiyah', string='Nama Liqo/UPPA', readonly=True)
    murobhi             = fields.Many2one(comodel_name="pks_anggota",  string="Murobhi",  help="", readonly=True)

    #Jenjang Tarbiyah
    last_jenjang        = fields.Selection(string='Tarbiyah', selection=[('pendukung', 'Pendukung'), ('penggerak', 'Penggerak'),('pelopor', 'Pelopor'),])
    jenjang_tarbiyah    = fields.Many2one(comodel_name='jenjang_tarbiyah', string='Jenjang Anggota')
    
    # tarbiyah1           = fields.Char(string='')
    
    tarbiyah1_ids       = fields.One2many(comodel_name="tarbiyah",  inverse_name="anggota_id",  string="Jenjang Pendukung", domain=[('jenjang_id.kategori','=','pendukung')], ondelete='cascade',  help="")
    tarbiyah2_ids       = fields.One2many(comodel_name="tarbiyah",  inverse_name="anggota_id",  string="Jenjang Penggerak", domain=[('jenjang_id.kategori','=','penggerak')], ondelete='cascade', help="")
    tarbiyah3_ids       = fields.One2many(comodel_name="tarbiyah",  inverse_name="anggota_id",  string="Jenjang Pelopor", domain=[('jenjang_id.kategori','=','pelopor')], ondelete='cascade', help="")

    pekerjaan_id        = fields.Many2one(comodel_name="ref_pekerjaan",  string="Pekerjaan",  help="")
    pendidikan_id       = fields.Many2one(comodel_name="ref_pendidikan",  string="Pendidikan",  help="")
    keluarga_ids        = fields.One2many(comodel_name="pks_keluarga",  inverse_name="anggota_id",  string="Keluarga", ondelete='cascade', help="")


    spouse_nama         = fields.Many2one(comodel_name='pks_anggota', string='Nama Suami/Istri')
    spouse_jns_kelamin  = fields.Selection(selection=[('laki-laki','Laki-Laki'),('perempuan','Perempuan')], related="spouse_nama.jns_kelamin", string="Jns kelamin", help="")
    spouse_tmp_lahir    = fields.Char( string="Tmp lahir", related="spouse_nama.tmp_lahir",  help="")
    spouse_tgl_lahir   = fields.Date( string="Tgl lahir", related="spouse_nama.tgl_lahir",  help="")
    spouse_mobile       = fields.Char(string='Nomor HP', related="spouse_nama.mobile", help="")
    spouse_pekerjaan_id = fields.Many2one(comodel_name="ref_pekerjaan",  string="Pekerjaan", related="spouse_nama.pekerjaan_id",  help="")
    spouse_pendidikan_id= fields.Many2one(comodel_name="ref_pendidikan",  string="Pendidikan", related="spouse_nama.pendidikan_id",  help="")

    spouse_last_jenjang = fields.Selection(string='Jenjang Tarbiyah', selection=[('pendukung', 'Pendukung'), ('penggerak', 'Penggerak'),('pelopor', 'Pelopor'),])
    sp_tarbiyah1a_date  = fields.Date(string='Jenjang Pemula')
    sp_tarbiyah1b_date  = fields.Date(string='Jenjang Siaga')
    sp_tarbiyah2a_date  = fields.Date(string='Jenjang Pratama')
    sp_tarbiyah2b_date  = fields.Date(string='Jenjang Muda')
    sp_tarbiyah3a_date  = fields.Date(string='Jenjang Madya')
    sp_tarbiyah3b_date  = fields.Date(string='Jenjang Dewasa')
    sp_tarbiyah3c_date  = fields.Date(string='Jenjang Utama')

    # Dokumen KTP
    dokumen_ktp         = fields.Binary(string='Dokumen KTP')
    dokumen_name        = fields.Char(string="Nama File KTP")

    # Dokumen KTA
    dokumen_kta         = fields.Binary(string='Dokumen KTA')
    dokumen_name_kta    = fields.Char(string="Nama File KTA")
    
    
    
    @api.onchange('kota_id')
    def _onchange_kota_id(self):
        self.city = self.kota_id.name

    @api.onchange('last_jenjang')
    def _onchange_last_jenjang(self):
        self.jenjang_tarbiyah = ''

    @api.onchange('tg_sesuai_ktp')
    def _onchange_tg_sma_ktp(self):
        if (self.tg_sesuai_ktp) and (self.tg_sesuai_ktp == '1'):
            self.tg_propinsi_id = self.propinsi_id
            self.tg_kota_id     = self.kota_id
            self.tg_kecamatan_id= self.kecamatan_id
            self.tg_desa_id     = self.desa_id
            self.tg_street2     = self.street2
            self.tg_street      = self.street
    
    @api.onchange('ada_kta')
    def _onchange_ada_kta(self):
        if self.ada_kta == '0':
            self.no_kta = ''
    
    # Open tampilan Aktivitas Liqo
    
    def open_aktivitas_liqo(self):
        return {
            'name'  : _('Aktivitas Liqo'),
            'domain' : [('name','=',self.id)],
            'view_type' : 'form',
            'res_model' : 'absen_liqo.line',
            'view_id' : False,
            'view_mode': 'tree,form',
            'type':'ir.actions.act_window'
        }
    
    def get_aktivitas_liqo_count(self):
        count = self.env['absen_liqo.line'].search_count([('name','=', self.id)])
        self.aktivitas_liqo_count = count
    
    # Field Jumlah Aktivitas
    aktivitas_liqo_count        = fields.Integer(string='Liqo Tarbiyah', compute='get_aktivitas_liqo_count')

    def get_saldo_iwai(self):
        saldo_iwai                  = self.env['tabungan_pks'].search([('anggota_id','=',self.id),('state','not in',['draft','cancel']),('jenis_tabungan','=','iwai')])
        self.saldo_tabungan_iwai    = sum((item.amount_in - item.amount_out) for item in saldo_iwai)

    def open_tabungan_iwai(self):
        return {
            'name'  : _('Tabungan IWAI'),
            'domain' : [('anggota_id','=',self.id),('jenis_tabungan','=','iwai')],
            'view_type' : 'form',
            'res_model' : 'tabungan_pks',
            'view_id' : False,
            'view_mode': 'tree,form',
            'type':'ir.actions.act_window'
        }

    # Field Saldo Tabungan
    saldo_tabungan_iwai         = fields.Float(string='Saldo IWAI', compute='get_saldo_iwai')
    
    def get_saldo_tapilu(self):
        saldo_tapilu                 = self.env['tabungan_pks'].search([('anggota_id','=',self.id),('state','not in',['draft','cancel']),('jenis_tabungan','=','tapilu')])
        self.saldo_tabungan_tapilu    = sum((item.amount_in - item.amount_out) for item in saldo_tapilu)

    def open_tabungan_tapilu(self):
        return {
            'name'  : _('Tabungan PEMILU'),
            'domain' : [('anggota_id','=',self.id),('jenis_tabungan','=','tapilu')],
            'view_type' : 'form',
            'res_model' : 'tabungan_pks',
            'view_id' : False,
            'view_mode': 'tree,form',
            'type':'ir.actions.act_window'
        }

    # Field Saldo Tabungan
    saldo_tabungan_tapilu         = fields.Float(string='Saldo TAPILU', compute='get_saldo_tapilu')

    # Field Rekrutmen
    rekrutmen_id                  = fields.Many2one(comodel_name='rekruitmen_pks', string='Rekrutmen ID', store=True)
    tgl_rekrutmen                 = fields.Date(string='Tanggal Rekrutmen', related='rekrutmen_id.tanggal')
    jns_rekrutmen                 = fields.Selection(string='Jenis Rekrutmen', selection=[('upa', 'UPA'), ('bidang', 'Bidang'),('dpc','DPC')], related='rekrutmen_id.jns_rekruitmen', store=True)
    bidang_id                     = fields.Many2one(comodel_name='bidang_pks', string='Nama Bidang', related='rekrutmen_id.bidang_id', store=True)
    upa_id                        = fields.Many2one(comodel_name='kelas_tarbiyah', string='Nama UPA', related='rekrutmen_id.upa_id', store=True)
    dpc_id                        = fields.Many2one(comodel_name='struktural_pks', string='Nama DPC', related='rekrutmen_id.dpc_id', store=True)
    #rekruiter                     = fields.Many2one(comodel_name='pks_anggota', string='Direkruit Oleh', related='rekrutmen_id.rekruiter')

    # def action_active(self):
    #     self.active = True

    # Riwayat Mutasi Anggota
    mutasi_id                     = fields.Many2one(comodel_name='mutasi_pks', string='Riwayat Mutasi')
    tgl_mutasi                    = fields.Date(string='Tanggal Mutasi', related='mutasi_id.tanggal')
    alamat_mutasi                 = fields.Char(string='Alamat Mutasi', related='mutasi_id.alamat')
    jns_mutasi                    = fields.Selection(string='Jenis Mutasi', selection=[('in', 'Mutasi Masuk'), ('out', 'Mutasi Keluar'),], related='mutasi_id.jns_mutasi')
    
    propinsi_mutasi               = fields.Many2one(comodel_name='ref.propinsi', string='Propinsi', related='mutasi_id.propinsi_id')
    kota_mutasi                   = fields.Many2one(comodel_name='ref.kota', string='Kabupaten/Kota', related='mutasi_id.kota_id')
    kecamatan_mutasi              = fields.Many2one(comodel_name='ref.kecamatan', string='Kecamatan', related='mutasi_id.kecamatan_id')
    desa_mutasi                   = fields.Many2one(comodel_name='ref.desa', string='Desa/Kelurahan', related='mutasi_id.desa_id')
    
    
    
    
    
    
    
    
    
