#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pks_tarbiyah(models.Model):

    _name               = "tarbiyah"
    _description        = "Pendataan Tarbiyah"
    _rec_name           = "jenjang_id"

    #name                = fields.Char( required=True, string="Name",  help="")
    tanggal             = fields.Date( string="Tanggal", required=True, help="")
    jenjang_id          = fields.Many2one(comodel_name='jenjang_tarbiyah', string='Jenjang', required=True)
    kategori            = fields.Selection(string='Kategori', selection=[('pendukung', 'Pendukung'), ('penggerak', 'Penggerak'),('pelopor', 'Pelopor'),],related='jenjang_id.kategori')
    keterangan          = fields.Text(string='Keterangan')
    
    anggota_id          = fields.Many2one(comodel_name="pks_anggota",  string="Anggota",  help="")
    _sql_constraints    = [('tarbiyah_uniq', 'unique(anggota_id,jenjang_id)', 'Data Jenjang Tarbiyah sudah ada !')]

class pks_jenjang_tarbiyah(models.Model):
    _name               = "jenjang_tarbiyah"
    _description        = "Jenjang Tarbiyah"

    name                = fields.Char(string="Jenjang", required=True)
    kategori            = fields.Selection(string='Kategori', selection=[('pendukung', 'Pendukung'), ('penggerak', 'Penggerak'),('pelopor', 'Pelopor'),], required=True, default="pendukung")
    _sql_constraints    = [('jenjang_tarbiyah_uniq', 'unique(name)', 'Data Jenjang Tarbiyah sudah ada !')]
    
class kelas_tarbiyah(models.Model):
    _name               = 'kelas_tarbiyah'
    _description        = 'Kelas / Kelompok Tarbiyah UPA'

    name                = fields.Char(string='Nama Liqo')
    keterangan          = fields.Char(string='Keterangan')
    
    murobhi             = fields.Many2one(comodel_name='pks_anggota', string='Murobhi')
    tarbiyah_ids        = fields.Many2many('pks_anggota','anggota_tarbiyah','anggota_id','partner_id','Anggota Tarbiyah')

    _sql_constraints    = [('kelas_tarbiyah_uniq', 'unique(name)', 'Nama Tarbiyah Liqo tersebut sudah ada !')]
    
    #@api.one
    def update_halaqoh(self):
        for x in self.tarbiyah_ids:
            x.write({'halaqoh_id': self.id, 
                'murobhi' : self.murobhi
            })
        return True


    

    
