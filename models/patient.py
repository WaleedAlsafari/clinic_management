from odoo import models, fields


class Patient(models.Model):
    _name = 'clinic_.patient'

    medical_file_no = fields.Char(required=True)
    date_of_birth = fields.Date(required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female','Female'),
    ], required=True )
    blood_type = fields.Selection([
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-'),
    ], required=True )
    insurance_no = fields.Char(required=True)
    emergency_contact = fields.Char(required=True)