from odoo import models, fields


class Doctors(models.Model):
    _name='hms.doctors'
    doctorfirstname=fields.Char(string='First Name')
    doctorlastname=fields.Char(string='Last Name')
    doctorimages=fields.Image(string='Doctor Images')
