#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pks_keluarga(models.Model):

    _name               = "pks_keluarga"
    _description        = "Pendataan Keluarga"

    name                = fields.Char( required=True, string="Name",  help="")
    jns_kelamin         = fields.Selection(selection=[('laki-laki','Laki-Laki'),('perempuan','Perempuan')],  string="Jenis kelamin", required=True,  help="")
    
    tmp_lahir           = fields.Char( string="Tempat lahir",  help="")
    tgl_lahir           = fields.Date( string="Tanggal lahir",  help="")

    anggota_id          = fields.Many2one(comodel_name="pks_anggota",  string="Orang Tua", required=True, help="")
    alamat              = fields.Char(string='Alamat Tinggal', related="anggota_id.tg_street")
    alamat2             = fields.Char(string='RT/RW', related="anggota_id.tg_street2")
    propinsi_id         = fields.Many2one(comodel_name='ref.propinsi', string='Propinsi', related="anggota_id.tg_propinsi_id")
    kota_id             = fields.Many2one(comodel_name='ref.kota', string='Kabupaten/Kota', related="anggota_id.kota_id")
    kecamatan_id        = fields.Many2one(comodel_name='ref.kecamatan', string='Kecamatan', related="anggota_id.tg_kecamatan_id")
    desa_id             = fields.Many2one(comodel_name='ref.desa', string='Desa/Kelurahan', related="anggota_id.tg_desa_id")
    jenjang_id          = fields.Many2one(comodel_name='jenjang_tarbiyah', string='Jenjang Tarbiyah')
    

    
