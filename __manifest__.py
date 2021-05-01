#-*- coding: utf-8 -*-

{
	"name": "anggota_pks",
	"version": "14.1.0", 
	"depends": [
		'base',
		'mail',
	],
	"author": "Cendana2000",
	"category": "Utility",
	"website": "http://cendana2000.co.id",
	"images": ["static/description/images/main_screenshot.jpg"],
	"price": "10",
	"license": "LGPL-3",
	"summary": "Aplikasi Manajemen Keanggotaan PKS",
	"description": """

Fitur-Fitur
======================================================================

* Menu Anggota : Pendataan Anggota, Aktivitas Tarbiyah
* Menu Keuangan : Iuran Wajib, Tabungan Pemilu
* Dashboard Laporan
* Pengaturan : Setting Konfigurasi, Master Data Referensi

""",
	"data": [
		"security/groups.xml",
		"security/ir.model.access.csv",
		"view/menu.xml",
		"view/pks_anggota.xml",
		"view/pekerjaan.xml",
		"view/pendidikan.xml",
		"view/pks_tarbiyah.xml",
		"view/pks_keluarga.xml",
		"view/jenjang_tarbiyah.xml",
		"view/ref_data_wilayah.xml",
		"view/aktivitas.xml",
		"view/struktural.xml",
		"view/keuangan.xml",
		"report/pks_anggota.xml",
		"report/pekerjaan.xml",
		"report/pendidikan.xml",
		"report/pks_tarbiyah.xml",
		"report/pks_keluarga.xml",
	],
	"installable": True,
	"auto_install": True,
	"application": True,
}