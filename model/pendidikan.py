#!/usr/bin/python
#-*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, Warning

class pendidikan(models.Model):

    _name               = "ref_pendidikan"
    _description        = "Tabel Referensi Pendidikan"

    name                = fields.Char( required=True, string="Name",  help="")
    keterangan          = fields.Char( string="Keterangan",  help="")
    active              = fields.Boolean( string="Active", default=True, help="")


