from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class ref_data(models.Model):
    _name           = "cdn.ref_data"
    _description    = "cdn.ref_data"

    name            = fields.Char( required=True, string="Name",  help="")
    jns_ref         = fields.Char( string="Jns ref",  help="")
    keterangan      = fields.Char( string="Keterangan",  help="")
    active          = fields.Boolean( string="Active",  help="")

class propinsi(models.Model):
    _name           = "ref.propinsi"
    _description    = "Referensi Propinsi"

    name            = fields.Char( required=True, string="Name",  help="")
    singkatan       = fields.Char( string="Singkatan",  help="")
    description     = fields.Text( string="Deskripsi",  help="")


    kota_ids        = fields.One2many(comodel_name="ref.kota",  inverse_name="propinsi_id",  string="Kota",  help="")

class kota(models.Model):
    _name           = "ref.kota"
    _description    = "Referensi Kota"

    name            = fields.Char( required=True, string="Name",  help="")
    singkatan       = fields.Char( string="Singkatan",  help="")
    description     = fields.Text( string="Deskripsi",  help="")


    propinsi_id     = fields.Many2one(comodel_name="ref.propinsi",  string="Propinsi",  help="")
    kecamatan_ids   = fields.One2many(comodel_name="ref.kecamatan",  inverse_name="kota_id",  string="Kecamatan",  help="")

class kecamatan(models.Model):
    _name           = "ref.kecamatan"
    _description    = "Referensi Data Kecamatan"

    name            = fields.Char( required=True, string="Name",  help="")
    description     = fields.Text( string="Deskripsi",  help="")


    kota_id         = fields.Many2one(comodel_name="ref.kota",  string="Kota",  help="")
    desa_ids        = fields.One2many(comodel_name="ref.desa",  inverse_name="kecamatan_id",  string="Desa",  help="")


class desa(models.Model):
    _name           = "ref.desa"
    _description    = "Referensi Data Desa"

    name            = fields.Char( required=True, string="Name",  help="")
    description     = fields.Text( string="Description",  help="")


    kecamatan_id    = fields.Many2one(comodel_name="ref.kecamatan",  string="Kecamatan",  help="")