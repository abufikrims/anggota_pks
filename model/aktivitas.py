from odoo import models, fields, api, exceptions, _


class absensi_liqo(models.Model):
    _name               = 'absensi_liqo'
    _description        = 'Tabel Aktivitas absensi Liqo'

    name                = fields.Date(string='Tanggal', required=True, default=fields.Date.context_today)
    halaqoh_id          = fields.Many2one(comodel_name='kelas_tarbiyah', string='Nama Liqo', required=True)
    murobhi             = fields.Many2one(comodel_name='pks_anggota', string='Murobhi', related="halaqoh_id.murobhi")
    amin_liqo           = fields.Many2one(comodel_name='pks_anggota', string="Amin Liqo'", related="halaqoh_id.amin_liqo")
    suun_maal           = fields.Many2one(comodel_name='pks_anggota', string="Suun Maal", related="halaqoh_id.suun_maal")

    absensi_lines       = fields.One2many(comodel_name='absen_liqo.line', inverse_name='absen_line_id', string='Daftar Kehadiran')
    
    keterangan          = fields.Text(string='Keterangan')
    state               = fields.Selection(selection=[('draft','Draft'),('proses','Proses'),('done','Selesai')],  string="Status",  help="Klik Done - untuk membuat daftar absensi tahfidz dan aktivitas nya") 
    
    _sql_constraints = [('absen_liqo_uniq', 'unique(name, halaqoh_id)', 'Data Absensi untuk hari tersebut sudah diinputkan - Silakan Cek Kembali !')]

    
    @api.onchange('halaqoh_id')
    def onchange_halaqoh_id(self):
        if self.halaqoh_id:
            for rec in self:
                anggota = [(5,0,0)]
                #self.absensi_lines = [(5,0,0)]
                for x in self.halaqoh_id.tarbiyah_ids:
                    val = {
                        'name': x.id,
                        'kehadiran': 'hadir'
                    }
                    anggota.append((0,0,val))
                rec.absensi_lines = anggota

    @api.model
    def create(self, vals):
        vals['state'] = 'draft'
        return super(absensi_liqo,self).create(vals)

    def action_done(self):
        return self.write({'state': 'done'})
    
    def action_proses(self):
        return self.write({'state': 'proses'})

class absen_liqo_line(models.Model):
    _name               = 'absen_liqo.line'
    _description        = 'Tabel Detail Absensi Anggota Liqo'

    absen_line_id       = fields.Many2one(comodel_name='absensi_liqo', string='Tanggal', required=True, ondelete='cascade')
    name                = fields.Many2one(comodel_name='pks_anggota', string='Nama Anggota')
    no_kta              = fields.Char(string='No KTA', related='name.no_kta')
    halaqoh_id          = fields.Many2one(comodel_name='kelas_tarbiyah', string='Nama Liqo', related='name.halaqoh_id')
    kehadiran           = fields.Selection(string='Kehadiran', selection=[('hadir', 'Hadir'), ('sakit', 'Sakit'),  ('ijin', 'Ijin'),  ('alpa', 'Alpa'), ])
    keterangan          = fields.Char(string='Keterangan')
    
    
    
    

