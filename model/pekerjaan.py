#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pekerjaan(models.Model):
    _name               = "ref_pekerjaan"
    _description        = "Tabel Referensi Pekerjaan"

    name                = fields.Char( required=True, string="Name",  help="")
    keterangan          = fields.Char( string="Keterangan",  help="")
    active              = fields.Boolean( string="Active", default=True, help="")


