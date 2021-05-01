from datetime import datetime
from odoo import api, fields, models, _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

STATES = [('draft','Konsep'),('confirm','Konfirmasi'),('done','Selesai')]

class tabungan_pks(models.Model):
    _name               = 'tabungan_pks'
    _description        = 'Tabel Tabungan PKS'

    name                = fields.Char(string="No. Referensi",  help="", readonly=True, default='Auto')
    anggota_id          = fields.Many2one(comodel_name='pks_anggota', string='Anggota PKS', readonly=True, states={"draft" : [("readonly",False)]},  help="")
    tanggal             = fields.Date(string='Tanggal', required=True, default=fields.Date.context_today, readonly=True, states={"draft" : [("readonly",False)]},  help="")
    amount_in           = fields.Float('Nominal Masuk', readonly=True, states={"draft" : [("readonly",False)]},  help="")
    amount_out          = fields.Float('Nominal Keluar', readonly=True, states={"draft" : [("readonly",False)]},  help="")
    deskripsi           = fields.Char(string='Deskripsi', readonly=True, states={"draft" : [("readonly",False)]},  help="")
    jenis_tabungan      = fields.Selection(string='Jenis Tabungan', selection=[('iwai', 'IWAI'), ('tapilu', 'TAPILU'),  ('sosial', 'SOSIAL'),], readonly=True, states={"draft" : [("readonly",False)]},  help="")
    jenis_setoran       = fields.Many2one(comodel_name='jenis_setoran', string='Jenis Setoran', readonly=True, states={"draft" : [("readonly",False)]},  help="")
    
    
    # State - Status Dokumen
    state               = fields.Selection(selection=STATES,  readonly=True, default=STATES[0][0],  string="Status",  help="")

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('tabungan_pks')
        return super(tabungan_pks, self).create(vals)

    def action_confirm(self):
        self.state = STATES[1][0]

    def action_selesai(self):
        self.state = STATES[2][0]

    def action_draft(self):
        self.state = STATES[0][0]
    
class jenis_setoran(models.Model):
    _name               = 'jenis_setoran'
    _description        = 'Tabel Jenis Setoran'

    name                = fields.Char(string='Nama Setoran')
    jns_mutasi          = fields.Selection(string='Jenis Mutasi', selection=[('debet', 'DEBET'), ('kredit', 'KREDIT'),])
    


    
