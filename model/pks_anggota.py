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
    tmp_lahir           = fields.Char( string="Tmp lahir",  help="")
    tgl_lahir           = fields.Date( string="Tgl lahir",  help="")
    status_kawin        = fields.Selection(selection=[('menikah','Menikah'),('janda','Janda'),('duda','Duda'),('belum menikah','Belum Menikah')],  string="Status Kawin", required=True, help="")

    # Data Alamat
    #nama jalan dan rt_rw menggunakan field street dan street2 di model res.partner
    propinsi_id         = fields.Many2one(comodel_name='ref.propinsi', string='Propinsi')
    kota_id             = fields.Many2one(comodel_name='ref.kota', string='Kabupaten/Kota')
    kecamatan_id        = fields.Many2one(comodel_name='ref.kecamatan', string='Kecamatan')
    desa_id             = fields.Many2one(comodel_name='ref.desa', string='Desa/Kelurahan')


    #Jika Alamat Tinggal beda dengan KTP
    tg_sesuai_ktp       = fields.Selection(string='Tempat Tinggal', selection=[('1', 'Sesuai KTP'), ('0', 'Beda Lokasi Tinggal'),], required=True)
    
    tg_street           = fields.Char(string='Nama Jalan')
    tg_street2          = fields.Char(string='RT/RW')
    tg_propinsi_id      = fields.Many2one(comodel_name='ref.propinsi', string='Propinsi')
    tg_kota_id          = fields.Many2one(comodel_name='ref.kota', string='Kabupaten/Kota')
    tg_kecamatan_id     = fields.Many2one(comodel_name='ref.kecamatan', string='Kecamatan')
    tg_desa_id          = fields.Many2one(comodel_name='ref.desa', string='Desa/Kelurahan')

    murobhi             = fields.Many2one(comodel_name="pks_anggota",  string="Murobhi",  help="")
    amanah_struktural   = fields.Selection(selection=[('dpp','DPP'),('dpw','DPW'),('dpd','DPD'),('dpc','DPC'),('dpra','DPRa')],  string="Amanah Struktural",  help="")
    jabatan_struktural  = fields.Char( string="Jabatan Struktural",  help="")
    jabatan_yayasan     = fields.Char(string='Jabatan Yayasan', help='')
    amanah_masyarakat   = fields.Boolean( string="Amanah Kemasyarakatan",  help="")
    jabatan_masyarakat  = fields.Char( string="Jabatan Masyarakat",  help="")
    ada_kta             = fields.Selection(string='Sudah Ber KTA', selection=[('1', 'YA'), ('0', 'TIDAK/BELUM'),], required=True, default='0')
    no_kta              = fields.Char( string="No KTA",  help="")

    #Jenjang Tarbiyah
    last_jenjang        = fields.Selection(string='Jenjang Tarbiyah', selection=[('pendukung', 'Pendukung'), ('penggerak', 'Penggerak'),('pelopor', 'Pelopor'),])
    #jenjang_tarbiyah    = fields.Many2one(comodel_name='jenjang_tarbiyah', string='Jenjang Tarbiyah')
    
    # tarbiyah1           = fields.Char(string='')
    
    tarbiyah1_ids       = fields.One2many(comodel_name="tarbiyah",  inverse_name="anggota_id",  string="Jenjang Pendukung", domain=[('jenjang_id.kategori','=','pendukung')], ondelete='cascade',  help="")
    tarbiyah2_ids       = fields.One2many(comodel_name="tarbiyah",  inverse_name="anggota_id",  string="Jenjang Penggerak", domain=[('jenjang_id.kategori','=','penggerak')], ondelete='cascade', help="")
    tarbiyah3_ids       = fields.One2many(comodel_name="tarbiyah",  inverse_name="anggota_id",  string="Jenjang Pelopor", domain=[('jenjang_id.kategori','=','pelopor')], ondelete='cascade', help="")

    pekerjaan_id        = fields.Many2one(comodel_name="ref_pekerjaan",  string="Pekerjaan",  help="")
    pendidikan_id       = fields.Many2one(comodel_name="ref_pendidikan",  string="Pendidikan",  help="")
    keluarga_ids        = fields.One2many(comodel_name="pks_keluarga",  inverse_name="anggota_id",  string="Keluarga", ondelete='cascade', help="")


    spouse_nama         = fields.Char('Nama Suami/Istri')
    spouse_jns_kelamin  = fields.Selection(selection=[('laki-laki','Laki-Laki'),('perempuan','Perempuan')],  string="Jenis kelamin", help="")
    spouse_tmp_lahir    = fields.Char( string="Tmp lahir",  help="")
    spouse_tgl_lahir   = fields.Date( string="Tgl lahir",  help="")
    spouse_mobile       = fields.Char(string='Nomor HP')
    spouse_pekerjaan_id = fields.Many2one(comodel_name="ref_pekerjaan",  string="Pekerjaan",  help="")
    spouse_pendidikan_id= fields.Many2one(comodel_name="ref_pendidikan",  string="Pendidikan",  help="")

    spouse_last_jenjang = fields.Selection(string='Jenjang Tarbiyah', selection=[('pendukung', 'Pendukung'), ('penggerak', 'Penggerak'),('pelopor', 'Pelopor'),])
    sp_tarbiyah1a_date  = fields.Date(string='Jenjang Pemula')
    sp_tarbiyah1b_date  = fields.Date(string='Jenjang Siaga')
    sp_tarbiyah2a_date  = fields.Date(string='Jenjang Pratama')
    sp_tarbiyah2b_date  = fields.Date(string='Jenjang Muda')
    sp_tarbiyah3a_date  = fields.Date(string='Jenjang Madya')
    sp_tarbiyah3b_date  = fields.Date(string='Jenjang Dewasa')
    sp_tarbiyah3c_date  = fields.Date(string='Jenjang Utama')
    
    @api.onchange('kota_id')
    def _onchange_kota_id(self):
        self.city = self.kota_id.name

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
        
    
