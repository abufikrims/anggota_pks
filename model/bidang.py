from odoo import api, fields, models


class bidang(models.Model):
    _name           = 'bidang_pks'
    _description    = 'Tabel Bidang PKS'

    name            = fields.Char(string='Nama Bidang')
    keterangan      = fields.Char(string='Keterangan')


    
