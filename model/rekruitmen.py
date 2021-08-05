from odoo import api, fields, models
from datetime import datetime


class rekruitmen(models.Model):
    _name           = 'rekruitmen_pks'
    _description    = 'Tabel Rekruitmen'

    name            = fields.Char(string="No. Referensi",  help="", readonly=True, default='Auto')
    tanggal         = fields.Date(string='Tanggal', required=True, default=fields.Date.context_today)
    rekruiter       = fields.Many2one(comodel_name='pks_anggota', required=True, string='Direkruit Oleh')
    jns_rekruitmen  = fields.Selection(string='Jenis Rekrutmen', selection=[('individu', 'Individu'), ('bidang', 'Bidang'),], default='individu')
    anggota_ids     = fields.One2many(comodel_name='pks_anggota', inverse_name='rekrutmen_id', string='Daftar Anggota Rekrutmen')
    bidang_id       = fields.Many2one(comodel_name='bidang_pks', string='Nama Bidang')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('rekruitmen_pks')
        return super(rekruitmen, self).create(vals)

    
    
    
    

