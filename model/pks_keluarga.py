#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pks_keluarga(models.Model):

    _name               = "pks_keluarga"
    _description        = "Pendataan Keluarga"

    name                = fields.Char( required=True, string="Name",  help="")
    jns_kelamin         = fields.Selection(selection=[('laki-laki','Laki-Laki'),('perempuan','Perempuan')],  string="Jns kelamin", required=True,  help="")
    
    tmp_lahir           = fields.Char( string="Tmp lahir",  help="")
    tgl_lahir           = fields.Date( string="Tgl lahir",  help="")

    anggota_id          = fields.Many2one(comodel_name="pks_anggota",  string="Orang Tua",  help="")
