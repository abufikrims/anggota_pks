from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

# Inherit res.company untuk menambahkan Propinsi_ID dan Kota_ID utk default
class company_inherit(models.Model):
    _inherit            = 'res.company'

    propinsi_id         = fields.Many2one(comodel_name='ref.propinsi', string='Default Propinsi')
    kota_id             = fields.Many2one(comodel_name='ref.kota', string='Default Kota/Kab')

    
    

class struktural_pks(models.Model):
    _name               = 'struktural_pks'
    _description        = 'Tabel Jabatan Struktural DPC PKS Level Kecamatan'

    name                = fields.Char(string='Nama', readonly=True)

    #Fungsi untuk mendapatkan default Kota dari res.company
    def _default_kota(self):
        return self.env['res.company'].search([('id','=',1)]).kota_id
    
    kota_id             = fields.Many2one(comodel_name='ref.kota', string='Default Kota/Kab', default=_default_kota)
    kecamatan_id        = fields.Many2one(comodel_name='ref.kecamatan', string='Kecamatan')
    periode             = fields.Char(string='Periode')
    ketua               = fields.Many2one(comodel_name='pks_anggota', string='Ketua DPC')
    waketua             = fields.Many2one(comodel_name='pks_anggota', string='Wakil Ketua')
    sekretaris          = fields.Many2one(comodel_name='pks_anggota', string='Sekretaris DPC')
    wasekretaris        = fields.Many2one(comodel_name='pks_anggota', string='Wakil Sekretaris')
    bendahara           = fields.Many2one(comodel_name='pks_anggota', string='Bendahara DPC')
    wabendahara         = fields.Many2one(comodel_name='pks_anggota', string='Wakil Bendahara')
    struktural_lines    = fields.One2many(comodel_name='struktural_pks_lines', inverse_name='struktural_pks_id', string='Seksi-Seksi')
    

    @api.onchange('kecamatan_id')
    def _onchange_kecamatan(self):
        if self.kecamatan_id:
            self.name = "Susunan Pengurus DPC PKS - Kecamatan "+  str(self.kecamatan_id.name)

class struktural_pks_lines(models.Model):
    _name               = 'struktural_pks_lines'
    _description        = 'Tabel Detail Struktural by Sie Organisasi'

    struktural_pks_id   = fields.Many2one(comodel_name='struktural_pks', string='Struktural Seksi DPC')
    name                = fields.Many2one(comodel_name='seksi_organisasi', string='Seksi')
    anggota_id          = fields.Many2one(comodel_name='pks_anggota', string='Nama')
    jabatan_sie         = fields.Selection(string='Jabatan', selection=[('ketua', 'Ketua'), ('wakil ketua', 'Wakil Ketua'), ('sekretaris', 'Sekretaris'), ('bendahara', 'Bendahara'), ('anggota', 'Anggota') ,])
    

class seksi_organisasi(models.Model):
    _name               = 'seksi_organisasi'
    _description        = ' Tabel Seksi Organisasi'
    
    name                = fields.Char(string='Nama Jabatan')
    
    
    
